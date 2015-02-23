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
import django.contrib.humanize.templatetags.humanize as humanize


from tutor.templatetags import tutor_extras
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

    tags = sorted(list(set(tags)))
    context = {"tags": tags}
    
    return render(request, 'tutor/tags.html', context)

def tests_to_json(test_results, admin_mode=False):
    tests = []
    for test, fail, result in test_results:
        data = {"id": test.id, "code": test.to_code(), "admin_mode": admin_mode}
        if fail is None:
            data["passed"] = True
            data["css_status"] = "success"
            data["status"] = "Pass"
            data["error_msg"] = ''
        else:
            data["passed"] = False
            data["status"] = "Fail"
            data["css_status"] = "danger"
            data["error_msg"] = tutor_extras.error_msg(fail)
        tests.append(data)

    return json.dumps(tests)



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
        passed, test_results = question.run_tests()

        if question.status == Question.FAILED:
            qstate = "danger"
        elif question.status == Question.ACTIVE:
            qstate = "success"
        else:
            qstate = "warning"

        if len(test_results) == 0:
            msg = """This question has no unit tests. 
            Without tests, this question can't be studied!"""

            messages.warning(request, msg)

    test_form = TestForm()
    os_ctrl = "ctrl"
    # if "Macintosh" in request.META["HTTP_USER_AGENT"]:
    #     os_ctrl = "cmd"

 
    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                # "tests": test_results,
                "qstate": qstate,
                "os_ctrl": os_ctrl,
                "question_json": form.instance.as_json(),
                "tests_json": tests_to_json(test_results,admin_mode=True)
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

    data = {}

    try:
        test = form.save()
        success = True

        user_function = q.solution
        test, ex, result = test.evaluate(user_function)
        passed = (ex == None)

        #update the question if the new test changed its status
        if q.status == Question.ACTIVE and not passed:
            q.status = Question.FAILED
            q.save()
        elif q.status == Question.ACTIVE and passed:
            q.status = Question.FAILED
            q.save()

        data['tests_json'] = tests_to_json([(test, ex, result)], admin_mode=True)
        data['question_json'] = q.as_json()

        if passed:
            data["message"] = {"msg": "Test added, code passed.", "msg_level": "success"}
        else:
            data["message"] = {"msg": "Test added, code failed.", "msg_level": "warning"}
        
        data["success"] = True

    except Exception as ex:
        data["message"] = {"msg": "Test code could not be added.", "msg_level": "danger"}
        data["success"] = False

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def del_test(request, pk):
    test = Test.objects.get(pk=pk)
    question = test.question
    if question.status == Question.DELETED:
        raise ValueError("Cannot delete tests to DELETED Questions")

    test.delete()
    msg = {"msg": "test deleted", "msg_level": "success"}
    updated = question.test_and_update()

    data = {"message": msg, "question_json": question.as_json()}
    return HttpResponse(json.dumps(data), content_type="application/json")



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
    data = {}
    try:
        question = form.save()

        results = []
        if pk > 0:
            passed, results = question.run_tests()
            if passed:
                question.status = Question.ACTIVE
            else:
                question.status = Question.FAILED

        pk = question.id
        question.save()
        archive(question)
        
        question_json = form.instance.as_json();
        data["question"] = question_json
        data["msg"] = {"msg": "question saved", "msg_level": "success"}
        # data["tests"] = json.dumps(results)

    except ValueError as vex:
        question_json = form.instance.as_json()
        data["msg"] = {"msg": "question saved", "msg_level": "success"}
        data["question"] = question_json
        data["form_erros"] = form.errors

    return HttpResponse(json.dumps(data), content_type="application/json")

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

    version = ArchiveQuestion.objects.get(parent__id=pk, version=versionNum)

    # question = Question.objects.get(pk=pk)
    question = version.parent

    question.function_name = version.function_name
    question.prompt = version.prompt
    question.solution = version.solution
    question.tags = version.tags
    question.level = version.level
    question.version = question.version + 1

    question.modifier = request.user

    question.comment = "Reverted to revision {} by {}".format(versionNum, request.user.username)
    question.test_and_update()
    archive(question)

    messages.success(request, "Question successfully reverted to revision {}.".format(versionNum))

    url = "/question/{}/edit".format(pk)

    return HttpResponseRedirect(url)




