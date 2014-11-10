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

import tutor.study as sm


@login_required
def study(request, try_again_id=0, study_tag=None):
    """Choose the next question for the user to study."""


    if try_again_id:
        question = Question.objects.get(pk=try_again_id)
    elif study_tag is not None:
        question = sm.next_question(request.user, study_tag)
    else:
        question = sm.next_question(request.user)

    response_form = ResponseForm()

    attempts = Response.objects.filter(user=request.user, question=question)[:Response.MAX_ATTEMPTS].count()
    attempt = attempts + 1
    attempts_left = Response.MAX_ATTEMPTS - attempts
    
    os_ctrl = "ctrl"
    if "Macintosh" in request.META["HTTP_USER_AGENT"]:
        os_ctrl = "cmd"
    context = {
        "question": question,
        "response_form" : response_form, 
        "attempt" : attempt,
        "attempts_left" : attempts_left,
        "tag" : study_tag,
        "os_ctrl": os_ctrl
    }
    
    return render(request, 'tutor/study.html', context)

@login_required
def respond(request):
    """Allow user to write a response to a question."""

    pk = int(request.POST["qpk"])
    user_code = request.POST.get('user_code', False)
    action = request.POST.get('action', 'foo')
    print("study code action:", action)
    study_tag = request.POST.get('study_tag', False)
    question = Question.objects.get(pk=pk)  

    passed, test_results = question.run_tests(user_code)    
    
    try:
        attempts = Response.objects.all().filter(user=request.user, question=question)
    except: 
        attempts = []
    
    response = Response(attempt=len(attempts) + 1, user=request.user, question=question)
    response.code = user_code
    #evaluate user's code
    response.is_correct = passed
    response.save()

    context = {"question" : question, 
               "response" : response, 
               "user_code": syn(user_code),
               "previous_attempt" : response.attempt - 1,
               "tests" : test_results,
               "passed" : passed,
               "study_tag": study_tag }

    
    
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
