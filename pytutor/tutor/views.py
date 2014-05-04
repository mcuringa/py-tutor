import random
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages

from tutor.models import *

@login_required
def study(request):
    """Randomly choose the next question for the user to study.
       If no questions exist, prompt the user to create one."""
    if request.method == "POST":
        respond(request)
    questions = Question.objects.all()
    if not questions:
        context = {"questions" : False}
    else:
        question = random.choice(questions)
        response_form = ResponseForm()
        context = {"question": question, "response_form" : response_form, "questions" : True}
        
    
    return render(request, 'tutor/respond.html', context)
    #except: 
    #    return HttpResponseRedirect("/tutor/no_questions")

@login_required
def no_questions(request):
    return render(request, 'tutor/no_questions.html')

@login_required
def respond(request):
    """Allow user to write a response to a question."""
    
    pk = int(request.POST["qpk"])
    #responses are linked to ArchiveQuestions, but we're given a Question key
    question = ArchiveQuestion.objects.all().filter(parent_id=pk).latest("created")

    #if the user has already attempted the question, use existing response object
    try:
        response = Response.objects.get(user=request.user, question=question)
        response.attempt += 1
    #if not, create one
    except: 
        response = Response(attempt=1, user=request.user, question=question)

    """Submit user's response for evaluation."""
    user_code = request.POST.get('code', False);
    response.code = user_code
    response.save()
    a = response.attempt - 1
    context = {"question" : question, "response" : response, "previous_attempt" : a}
    #evaluate user's code
    testResults = []
    passAll = False
    for test in Test.objects.all().filter(question=pk):
        result = test.evaluate(user_code)
        testResults.append( (test, result[0]) )
        passAll = result[1] and True

    context["testResults"] = testResults
    if not passAll:
        return render(request, 'tutor/response_incorrect.html', context)
    #so if there are no tests, the response defaults to being marked correct.
    return render(request, 'tutor/response_correct.html', context)

def list(request):
    """List the questions in the database"""
    
    questions = Question.objects.all()
    context = {"questions": questions}
    
    return render(request, 'tutor/list.html', context)

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
        test_results = {}
        if tests.count() == 0:
            messages.add_message(request, messages.INFO, 'This question has no unit tests. Without unit tests, a response to this question won\'t be properly evaluated. Create a unit test below!')
        else:
            for test in tests:
                if test.evaluate()[1] == False:
                    messages.add_message(request, messages.INFO, 'Test ' + str(test.to_code()) + ' failed on Solution code. Check this test case and your solution code to fix the issue.')
                    result = "Test failed on 'Solution' code."
                    passed = False
                else:
                    result = "Test passed on 'Solution' code!"
                    passed = True
                test_results[test.pk] = (test.to_code(), result, passed)

    test_form = TestForm()

    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                "tests": test_results
              }

    return render(request, 'tutor/question_form.html', context)

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
    return HttpResponseRedirect("/tutor/list")

def archive(question):
    aq = ArchiveQuestion()
    aq.archive(question)
    aq.modifier = question.modifier
    aq.save()

@login_required
def add_test(request):
    questionId = int(request.POST["question_id"])
    q = Question.objects.get(pk=questionId)
    form = TestForm(request.POST)
    form.instance.question = q
    try:
        test = form.save()
        success = True

    except:
        message = "Tests require arguments, expected results, and a fail message."
        success = False
        passed = False
        list_append = ""

    if success:
        message = ""
        user_function = test.question.solution
        result = test.evaluate(user_function)
        if result[1]:
            #this test passed
            passed = True
            list_append = "<li class=\"bg-success\">" + test.to_code() + "<br>Result: Test passed on 'Solution' code!<br>" + "<a href=\"/tutor/test/" + str(test.id) + "/del\" alt=\"Delete this test\">x</li>"
        else:
            #this test didn't
            passed = False
            list_append = "<li class=\"bg-danger\">" + test.to_code() + "<br>Result: Test failed on 'Solution' code.<br>" + "<a href=\"/tutor/test/" + str(test.id) + "/del\" alt=\"Delete this test\">x</li>"
    data = {
        "success": success,
        "message": message,
        "list_append": list_append,
        "passed": passed
    }
    # json = serializers.serialize("json", [test])
    # # return a sustring because djano only works with
    # # iterables, but we just want a single json object
    # data = json[1:-1]

    return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def del_test(request, pk):
    test = Test.objects.get(pk=pk)
    question = test.question
    test.delete()
    messages.add_message(request, messages.INFO, "Test successfully deleted.")
    url = "/tutor/" + str(question.id) + "/edit"
    return HttpResponseRedirect(url)


