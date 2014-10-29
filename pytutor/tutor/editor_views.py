import random
import json

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

        context["editor_name"] =  editor_name
        print("context:", context)
        questions = Question.objects.all().filter(Q(creator__username=editor_name) | Q(modifier__username=editor_name)).order_by('-modified')

    else:
        editor_name = "All"
        questions = Question.objects.all().order_by('-modified')

    
    context["questions"] = questions

    
    return render(request, 'tutor/list.html', context)

def tags(request):
    """List the tags in the database"""
    
    questions = Question.objects.all()
    tags = []
    for question in questions:
        qtags = question.tags.split(",")
        qtags = [q.strip() for q in qtags]
        tags.extend(qtags)

    tags = set(tags)
    tags = sorted([t for t in tags])
    context = {"tags": tags}
    
    return render(request, 'tutor/tags.html', context)

@login_required
def question_form(request, pk=0):
    
    if pk == 0:
        form = QuestionForm()
        history = []
        test_results = []
    else:

        question = Question.objects.get(pk=pk)        
        form = QuestionForm(instance=question)
        #form.id_comment = "" #this doesn't actually clear the field
        history = ArchiveQuestion.objects.all().filter(parent_id=pk)
        tests = Test.objects.all().filter(question=question)
        test_results = [t.evaluate() for t in tests]

        if tests.count() == 0:
            messages.add_message(request, messages.INFO, 'This question has no unit tests. Without unit tests, a response to this question won\'t be properly evaluated. Create a unit test below!')

    test_form = TestForm()

    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                "tests": test_results
              }

    return render(request, 'tutor/question_form.html', context)


@login_required
def add_test(request):

    
    questionId = int(request.POST["question_id"])
    q = Question.objects.get(pk=questionId)
    form = TestForm(request.POST)
    form.instance.question = q
    try:
        test = form.save()
        success = True

        user_function = q.solution
        test, ex, result = test.evaluate(user_function)
        passed = ex == None

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
    print(json.dumps(data))

    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def save_question(request):

    print('saving a question...')
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
      archive(question)
      url = "/tutor/" + str(question.id) + "/edit"
    except:
        messages.add_message(request, messages.INFO, 'Please fill out all required fields.')
        url = "/tutor/new"


    return HttpResponseRedirect(url)


@login_required
def delete_question(request, pk):
    """Deletes the selected question and all related ArchiveQuestions."""

    question = Question.objects.get(pk=pk)
    archives = ArchiveQuestion.objects.all().filter(parent_id=pk)
    for q in archives:
        q.delete()
    question.delete()

    messages.success(request, "Question deleted.")

    return HttpResponseRedirect("/tutor/list")

def archive(question):
    aq = ArchiveQuestion()
    aq.archive(question)
    aq.modifier = question.modifier
    aq.save()

@login_required
def del_test(request, pk):
    test = Test.objects.get(pk=pk)
    question = test.question
    test.delete()
    messages.success(request, "Test deleted.")
    url = "/tutor/" + str(question.id) + "/edit"
    return HttpResponseRedirect(url)


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

    messages.add_message(request, messages.INFO, "Test successfully duplicated.")
    url = "/tutor/" + str(new_q.id) + "/edit"

    return HttpResponseRedirect("/tutor/list")

