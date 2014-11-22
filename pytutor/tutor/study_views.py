import random
import json
from operator import itemgetter, attrgetter

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


def get_attempts(user, question):
    attempts = Response.objects.filter(user=user).order_by("-submitted")[:Response.MAX_ATTEMPTS]
    attempts = len([r for r in attempts if r.question == question])
    attempts_left = Response.MAX_ATTEMPTS - attempts
    return attempts, attempts_left


@login_required
def study(request, sticky_id=0, study_tag=None):
    """Choose the next question for the user to study."""

    sticky_id = int(sticky_id)

    if sticky_id > 0:
        question = Question.objects.get(pk=sticky_id)
    elif study_tag is not None:
        question = sm.next_question(request.user, study_tag)
    else:
        question = sm.next_question(request.user)

    attempts, attempts_left = get_attempts(request.user, question)

    if sticky_id > 0:
        user_code = attempts[0].code
    else:
        user_code = "# write a function called {}{}".format(question.function_name, "\n"*3)

    response_form = ResponseForm()
    
    os_ctrl = "ctrl"
    if "Macintosh" in request.META["HTTP_USER_AGENT"]:
        os_ctrl = "cmd"
    context = {
        "user_code": user_code,
        "question": question,
        "sticky_id": sticky_id,
        "response_form" : response_form, 
        "attempts_left" : attempts_left,
        "tag" : study_tag,
        "os_ctrl": os_ctrl
    }
    
    return render(request, 'tutor/study.html', context)

def solutions(request, questionId, context={}):

    if len(context) == 0:
        question = Question.objects.get(pk=questionId)
        tests = Test.objects.filter(question=question)
        response = Response.objects.filter(question=question, user=request.user).order_by("-submitted")[0]
        passed, test_results = question.run_tests(response.code)
    else:
        question = context["question"]

    user_solutions = Response.objects.filter(question=question, is_correct=True).values_list("code").distinct()
    expert_solutions = sorted(list(set(Solution.objects.filter(parent=question))), key=attrgetter('version'), reverse=True)
    for sol in expert_solutions:
        sol.test(tests)

    user_solutions = [syn(c[0]) for c in user_solutions]
    context = {
       "question": question,
       "response": response,
       "test_results": test_results,
       "passed": passed,
       "expert_solutions": expert_solutions,
       "user_code": user_solutions
    }
    return render(request, 'tutor/solutions.html', context)


@login_required
def respond(request):
    """Allow user to write a response to a question."""

    pk = int(request.POST["qpk"])
    user_code = request.POST.get('user_code', False)
    sticky_id = int(request.POST.get('sticky_id,', 0))

    study_tag = request.POST.get('study_tag', False)
    question = Question.objects.get(pk=pk)  

    passed, test_results = question.run_tests(user_code)

    attempts, attempts_left = get_attempts(request.user, question)
    attempt = attempts + 1
    attempts_left -= 1
    
    response = Response(attempt=attempt, user=request.user, question=question)
    response.code = user_code
    response.is_correct = passed
    response.save()

    context = {"question" : question, 
               "response" : response, 
               "attempts_left" : attempts_left,
               "tests" : test_results,
               "passed" : passed,
               "sticky_id": sticky_id,
               "study_tag": study_tag }
    
    if attempts_left == 0 and sticky_id == 0:
        return solutions(request, question, response, context)

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
