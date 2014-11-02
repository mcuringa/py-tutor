import random
import json
import difflib

from django.template import loader, Context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.db.models import Q

from tutor.models import *

def list(request, editor_name=""):
    """List the questions in the database"""
    print ("editor:", editor_name)

    context = {}
    if len(editor_name) > 0:
        # filter the questions on this editor
        questions = Question.objects.all().filter(Q(creator__username=editor_name) | Q(modifier__username=editor_name)).order_by('-modified')
    else:
        editor_name = "All"
        questions = Question.objects.all().order_by('-modified')

    context["editor_name"] =  editor_name
    context["questions"] = questions
    
    return render(request, 'tutor/list.html', context)

def tags(request):
    """List the tags in the database"""
    
    questions = Question.objects.all()
    tags = []
    for question in questions:
        qtags = question.tags.split(",")
        qtags = [q.strip() for q in qtags if len(q.strip() > 0)]
        tags.extend(qtags)

    tags = set(tags)
    tags = sorted(list(tags))
    context = {"tags": tags}
    
    return render(request, 'tutor/tags.html', context)

@login_required
def question_form(request, pk=0):

    if pk == 0:
        form = QuestionForm()
        history = []
        test_results = []
        qstate = "default"
    else:

        question = Question.objects.get(pk=pk)        
        form = QuestionForm(instance=question)
        history = ArchiveQuestion.objects.all().filter(parent_id=pk).order_by('-version')
        tests = Test.objects.all().filter(question=question)
        test_results = [t.evaluate() for t in tests]

        if question.status == Question.FAILED:
            qstate = "danger"
        elif question.status == Question.ACTIVE:
            qstate = "success"
        else:
            qstate = "warning"


        if tests.count() == 0:
            msg = """This question has no unit tests. 
            Without unit tests, a response to this 
            question won't be properly evaluated. Create a unit test below!"""

            messages.warning(request, msg)



    test_form = TestForm()


    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                "tests": test_results,
                "qstate": qstate
              }

    return render(request, 'tutor/question_form.html', context)


@login_required
def add_test(request):

    questionId = int(request.POST["question_id"])
    q = Question.objects.get(pk=questionId)

    if q.status == Question.DELETED:
        raise ValueError("Cannot add tests to DELETED Questions")

    form = TestForm(request.POST)
    form.instance.question = q
    try:
        test = form.save()
        success = True

        user_function = q.solution
        test, ex, result = test.evaluate(user_function)
        passed = ex == None

        if q.status == Question.ACTIVE and not passed:
            print("failed test, update question")
            q.status = Question.FAILED
            q.save()

        c = Context({
            'test': test,
            'ex': ex,
            'result': result
        })

        t = loader.get_template('tutor/test-results.html')
        list_append = t.render(c)

    except:
        message = "Tests require expected results."
        success = False
        passed = False
        list_append = ""


    if passed:
        message = "Test added and passed."
        msg_level = "success"
    else:
        message = "Test added successfully, but code failed."
        msg_level = "warning"


    data = {
        "success": success,
        "msg": message,
        "list_append": list_append,
        "passed": passed,
        "msg_level": msg_level
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def del_test(request, pk):
    test = Test.objects.get(pk=pk)
    question = test.question
    test.delete()
    oldStatus = question.status
    active = question.update_status()
    msg = "Test deleted."
    if question.status != oldStatus:
        msg += " Status changed to {}.".format(question.status_label())
    messages.success(request, msg)
    url = "/question/{}/edit".format(question.id)
    return HttpResponseRedirect(url)

@login_required
def save_question(request):

    pk = int(request.POST["pk"])
    if pk > 0:
        q = Question.objects.get(pk=pk)
        form = QuestionForm(request.POST, instance=q)
        form.instance.version += 1
    else:
        form = QuestionForm(request.POST)
        form.instance.version = 1
        form.instance.creator = request.user

    form.instance.modifier = request.user
    try:
      question = form.save()
      pk = question.id
      print("question id:", pk)

      archive(question)
      messages.success(request, "Question saved.")
    except:
        messages.warning(request, 'Please fill out all required fields.')

    url = "/question/{}/edit".format(pk)

    return HttpResponseRedirect(url)

@login_required
def delete_question(request, pk):
    """Deletes the selected question and all related ArchiveQuestions."""

    question = Question.objects.get(pk=pk)
    responses = Response.objects.all().filter(question=question)
    archives = ArchiveQuestion.objects.all().filter(parent_id=pk).order_by('-version')

    if len(responses) == 0: # hard delete
        for q in archives:
            q.delete()
        question.delete()
        messages.success(request, "Question deleted.")
    else:
        question.status = Question.DELETED
        question.save()
        messages.success(request, "Question de-activated.")

    return HttpResponseRedirect("/question/list")

def archive(question):
    aq = ArchiveQuestion()
    aq.archive(question)
    aq.modifier = question.modifier
    aq.save()

@login_required
def dup(request, pk=0):
    new_q = Question.objects.get(pk=pk)
    tests = Test.objects.all().filter(question=new_q)
    new_q.pk = None
    new_q.creator = request.user
    new_q.modifier = request.user
    new_q.save()

    for t in tests:
        t.pk = None
        t.question = new_q
        t.save()

    messages.success(request, "Test successfully duplicated.")
    url = "/question/{}/edit".format(new_q.pk)

    return HttpResponseRedirect("/question/list")

def html_diff(s1, s2):
    ugly = difflib.HtmlDiff().make_table(s1.split("\n"), s2.split("\n"))

    return ugly


@login_required
def diff(request, pk, v1, v2):
    
    q1 = ArchiveQuestion.objects.get(parent__id=pk, version=v1)
    q2 = ArchiveQuestion.objects.get(parent__id=pk, version=v2)
    titles = html_diff(q1.function_name, q2.function_name)
    prompts = html_diff(q1.prompt, q2.prompt)
    solutions = html_diff(q1.solution, q2.solution)
    
    context = {
        "question": q1.parent,
        "versions": [q1,q2],
        "titles": titles,
        "prompts": prompts,
        "solutions": solutions,
    }
    return render(request, 'tutor/diff.html', context)


@login_required
def revert(request, pk, versionNum):
    print("pk:", pk)
    print("versionNum:", versionNum)

    version = ArchiveQuestion.objects.get(parent__id=pk, version=versionNum)
    print("version:", version.function_name)

    # question = Question.objects.get(pk=pk)
    question = version.parent
    print("question:", question)

    question.function_name = version.function_name
    question.prompt = version.prompt
    question.solution = version.solution
    question.tags = version.tags
    question.level = version.level
    question.version = question.version + 1

    question.modifier = request.user

    question.comment = "Reverted to revision {} by {}".format(versionNum, request.user.username)
    question.save()
    archive(question)

    messages.success(request, "Question successfully reverted to revision {}.".format(versionNum))

    url = "/question/{}/edit".format(pk)

    return HttpResponseRedirect(url)




