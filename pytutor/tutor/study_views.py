import random
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.db.models import Q

from pytutor.views import home

from tutor.templatetags.tutor_extras import syn
from tutor.models import *

@login_required
def study(request, try_again_id=0, study_tag=None):
    """Randomly choose the next question for the user to study.
       If no questions exist, prompt the user to create one."""

    questions = Question.objects.all()
    if not questions:
        messages.info(request, 'There are currently no questions to study.')
        return home(request)

    if try_again_id:
        question = Question.objects.get(pk=try_again_id)
    elif study_tag is not None:
        questions = Question.objects.filter(tags__icontains=study_tag) 
        question = random.choice(questions)
    else:
        question = serve_question(request.user)

    response_form = ResponseForm()
    try:
        response = Response.objects.get(user=request.user, question=question)
        attempt = response.attempt + 1
    except: 
        attempt = 1
    
    context = {
        "question": question,
        "response_form" : response_form, 
        "questions" : True,
        "attempt" : attempt,
        "tag" : study_tag
    }
    
    return render(request, 'tutor/respond.html', context)

@login_required
def respond(request):
    """Allow user to write a response to a question."""

    pk = int(request.POST["qpk"])
    user_code = request.POST.get('user_code', False)
    study_tag = request.POST.get('study_tag', False)
    question = Question.objects.get(pk=pk)  
    
    try:
        attempts = Response.objects.all().filter(user=request.user, question=question)
    except: 
        attempts = []
    
    response = Response(attempt=len(attempts) + 1, user=request.user, question=question)
    response.code = user_code

    #evaluate user's code
    
    testResults = []
    passed_tests = True
    for t in Test.objects.all().filter(question=pk):
        (test, ex, result) = t.evaluate(user_code)
        testResults.append((test, ex, result))
        if ex is not None and passed_tests:
            passed_tests = False

    response.is_correct = passed_tests

    context = {"question" : question, 
               "response" : response, 
               "user_code": syn(user_code),
               "previous_attempt" : response.attempt - 1,
               "tests" : testResults,
               "passed_tests" : passed_tests,
               "study_tag": study_tag }

    response.save()
    
    return render(request, 'tutor/response_result.html', context)

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


def serve_question(user):
    """Serves a user the next applicable question."""
    #get history of user's correct and incorrect responses
    # correct_responses = Response.objects.all().filter(user=user, is_correct=True)
    # incorrect_responses = Response.objects.all().filter(user=user, is_correct=False)

    questions = Question.objects.all().filter()
    next_q = random.choice(questions)
    return next_q
