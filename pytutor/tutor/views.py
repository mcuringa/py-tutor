import random
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

    try:
        question = random.choice(Question.objects.all())
        return respond(request, question.pk)
    except: 
        return HttpResponseRedirect("/tutor/no_questions")

@login_required
def no_questions(request):
    return render(request, 'tutor/no_questions.html')

@login_required
def respond(request, pk):
    """Allow user to write a response to a question."""
    
    #responses are linked to ArchiveQuestions, but we're given a Question key
    question = most_recent_version(Question.objects.get(pk=pk))
    
    #if the user has already attempted the question, use existing response object
    try:
        response = Response.objects.get(user=request.user, question=question)
    #if not, create one
    except: 
        response = Response(attempt=1, user=request.user, question=question)
        response.save() #is this necessary here?
    response_form = ResponseForm()
    context = {"question": question, "response" : response, "response_form" : response_form}
    
    return render(request, 'tutor/respond.html', context)

@login_required
def submit_response(request):
    """Submit user's response for evaluation."""
    qpk = int(request.POST["qpk"])
    rpk = int(request.POST["rpk"])
    question = Question.objects.get(pk=qpk);
    response = Response.objects.get(pk=rpk);
    
    response.attempt += 1
    user_code = request.POST["code"]
    response.code = user_code
    response.save() #again, is this necessary?
    a = response.attempt - 1
    context = {"question" : question, "response" : response, "previous_attempt" : a}
    #evaluate user's code
    testResults = []
    passAll = False
    for test in Test.objects.all().filter(question=qpk):
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
        history = ArchiveQuestion.objects.all().filter(parent_id=pk)
        tests = Test.objects.all().filter(question=question)
        test_results = {}
        for test in tests:
            if test.evaluate()[1] == False:
                result = "Test failed on 'Solution' code."
            else:
                result = "Test passed on 'Solution' code!"
            test_results[test.pk] = (test.to_code(), result)
        if Test.objects.all().filter(question=question).count() == 0:
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
    question = form.save()
    archive(question)
    
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
    test = form.save()
    user_function = test.question.solution
    print(user_function)
    test.evaluate(user_function)
    # json = serializers.serialize("json", [test])
    # # return a sustring because djano only works with
    # # iterables, but we just want a single json object
    # data = json[1:-1]

    return HttpResponse(test.to_code(), mimetype='text/plain')

def most_recent_version(question):
    all = ArchiveQuestion.objects.all().filter(parent_id=question.pk)
    most_recent = all[0]
    for q in all:
        if most_recent.modified < q.modified:
            most_recent = q
    return most_recent
