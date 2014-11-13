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
from django.db.models import Count

@login_required
def report(request):
# """List the correct and incorrect answers of the user"""
#     print ("student:", user_name)
    # student_responses=Question
    # user=request.user
    # level_questions = Question.objects.by_level()
    # print (level_questions)
    # for level, questions in level_questions.items():
    #     for q in questions:
    #         response = q.latest_response_for(user)
    #         result = 'not answered'
    #         if response is not None:
    #             result = str(response.is_correct)
    #         setattr(q, 'user_responded_correctly', result)

    user=request.user

# get all of the responses students have made.
# organize them by their level and list their question name.
    student_responses = Response.objects.all().filter(user=user).order_by("question__id")
    
    cur_id = -1 # the current question we're counting up
    rows = []
    data = {}
    right_count = 0
    wrong_count = 0

    for r in student_responses:
        q = r.question
        if q.id != cur_id: #start a new row
            # add the data as a row
            data["num_right"] = right_count
            data["num_wrong"] = wrong_count
            rows.append(data)
            cur_id = q.id

            # reset the data
            data = {}
            data["question"] = q
            right_count = 0
            wrong_count = 0
        if r.is_correct:
            right_count += 1
        else:
            wrong_count += 1


# # group the questions that have been answer correctly
#     correct_responses= [r for r in user_responses if r.is_correct]
#     incorrect_responses = [r for r in user_responses if not r.is_correct]
#     for response in user_responses:
#         if response.is_correct== True:
#             correct_responses.append(response)
#         else:
#             incorrect_responses.append(response)

# single table w all questions and whether you got it right or wrong.
# group by queries (django) don't do.

# map.. python, functools library.  take a list and apply function to every item and return one thing
    # # List questions that student has passed
    # questions_passed=Response.objects.all().filter(user=user, is_correct=True)
    # questions_failed=HttpResponse.objects.all().filter(user=user, is_correct=False)

    # context = {"questions_passed": questions_passed,
    #     "questions_failed": questions_failed}

    context = {"student_responses": rows[1:],
              
               }
    # List questions that student has failed
    return render(request, 'student/report.html', context)


def question_detail(request, question_id):
    user=request.user 
    question= Question.objects.get(pk=question_id)
    responses= Response.objects.all().filter(question=question, user=user)
    attempts= len(responses)
    unique = unique_responses(responses)

    context = { "question": question, "responses": unique, "attempts": attempts}

    return render ( request, 'student/question_detail.html', context)

def unique_responses(responses):
    unique_responses=[]
    for r in responses:
        if r.code not in unique_responses:
            unique_responses.append(r.highlighted_code())
    return unique_responses

def user_log(question):

    user = request.user
    responses = Response.objects.filter(user=user).order_by("question__id, -submitted")
    study_sessions = []
    qid = -1
    for r in responses:
        
        if r.question.id != qid:
            attempts = []
            quid = r.question.id
            study_sessions.append(attempts)
        attempts.append(r)
    return [s for s in study_sessions if s[0].question == question]

    # session = total responses for single question in a continuous block of time
    # WE ARE returning the single session for the latest question






