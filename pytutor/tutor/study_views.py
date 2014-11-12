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



def study(request, try_again_id=0, study_tag=None):
    """Choose the next question for the user to study."""

    if not request.user.is_authenticated():
        messages.info(request, "You must sign-up or log-in to study.")
        return HttpResponseRedirect("/register")

    if try_again_id:
        question = Question.objects.get(pk=try_again_id)
    elif study_tag is not None:
        question = sm.next_question(request.user, study_tag)
    else:
        question = sm.next_question(request.user)

    response_form = ResponseForm()

    attempts = Response.objects.filter(user=request.user)[:Response.MAX_ATTEMPTS]
    attempts = len([r for r in attempts if r.question == question])
    attempts_left = Response.MAX_ATTEMPTS - attempts
    
    os_ctrl = "ctrl"
    if "Macintosh" in request.META["HTTP_USER_AGENT"]:
        os_ctrl = "cmd"
    context = {
        "question": question,
        "response_form" : response_form, 
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

    study_tag = request.POST.get('study_tag', False)
    question = Question.objects.get(pk=pk)  

    passed, test_results = question.run_tests(user_code)    

    attempts = Response.objects.filter(user=request.user)[:Response.MAX_ATTEMPTS]
    attempts = len([r for r in attempts if r.question == question])
    attempt = attempts + 1
    attempts_left = Response.MAX_ATTEMPTS - attempt
    
    response = Response(attempt=attempt, user=request.user, question=question)
    response.code = user_code
    response.is_correct = passed
    response.save()

    context = {"question" : question, 
               "response" : response, 
               "attempts_left" : attempts_left,
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
