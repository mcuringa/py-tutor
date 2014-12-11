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
    correct_list = []
    incorrect_list = []

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

        # print ("This is data dict", data)

    # for r in student_responses:
    #     q = r.question
    #     if not q.is_correct:




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

def say_level_name(request):
    question = Question.objects.all()

    for q in question:
        print (q.level)
        if q.level == 1:
            level_name = "Level 1: Basics - simple functions, variables, operators."

        else:
            level_name= "not level 1"
    context = {"question": question,
                "level_name": level_name
                }
    return render(request, 'student/report.html', context)
              # cr = student_responses[0]
    # cur_q = cr.question
    # cur_l = cur_q.level()
    # if cur_l == 1:
    #     cur_l = "Level 1: Basics - simple functions, variables, operators."
    # elif cur_l == 2:
    #     cur_l = "Level 2: Basics - Conditional Statements, Built-In functions."
    # elif cur_l == 3:
    #     cur_l = "Level 3: Beginner - Strings, basics."
    # elif cur_l == 4:
    #     cur_l = "Level 4: Intermediate - Lists and loops"
    # elif cur_l == 5:
    #     cur_l = "Level 5: Upper Intermediate- Dictionaries, tuples, sets, string functions"
    # elif cur_l == 6: 
    #     cur_l = "Level 6: Advanced - Multi-step problems, libraries, OOP"
    # else:
    #     cur_l = "Level 7: Pro - Hard Problems"
    # print (cur_l)

def get_leveled_questions(request):
    solved_qs= []
    unsolved_qs = []
    user = request.user

    user_response = Response.objects.all().filter(user=user)

    for r in user_response:
        print (r)
        if r.is_correct:
            solved_qs.append(r)
            print (solved_qs)
        else:
            unsolved_qs.append(r)
            print (unsolved_qs)

    context = {"solved_qs": solved_qs,
                "unsolved_qs": unsolved_qs
                }
    return render(request, "student/report.html", context)

    # for r in user_response:
    #     for q in question_pool:
    #         if r.id == q.id:

    # quests = Question.objects.all()

    # for q in quests:
    #     level = q.level
    #     print (level)

    # context = {"quests": quests,
    #             "level": level,
    #             "qs": qs,
    #             }

    # return render(request, 'student/report.html', context)


def simple(request):
    user=request.user 
    res = Response.objects.all()[:3]
    for r in res:
        r1 = r[1]
        print (r1)

    context = {"r1": r1,
            }
    return render(request, 'student/report.html', context)








def organize_report(request):

    user = request.user
    all_responses = Response.objects.all().filter(user=user)
    all_questions = Question.objects.all()
    level_questions = Question.objects.by_level()

    print (level_questions)

    solved_question = []
    unsolved_question = []
   
    for r in all_responses:
        if r.question.is_correct:
            print(r.question.is_correct)
    # for q in all_questions:
    #     if q.response.is_correct:
            print ("This is working, while q.resp.is_correct")
            solved_question.append(r)
        else:
            unsolved_question.append(r)
    print ("this is a solved question", solved_question[1])
    
    # for r in all_responses:
    #     if r.is_correct== True:
    #         correct_responses.append(r)
    #     else:
    #         incorrect_responses.append(r)

    # for r in all_responses:
    #     for q in all_questions:
    #         if r.id == q.id:
    #             current_level = q.level()

    context = {"solved_question": solved_question,
                "unsolved_question": unsolved_question,
                # "level_questions": level_questions,
                
    }
    # print ("This is starting", solved_question)
    return render(request, 'student/report.html', context)
# def current_level(request):
#     user = request.user
#     questions = Question.objects.all().filter(user=user).order_by("-submitted")
#     cq= questions[0]
#     current_response = cq.response

#     cr_list = []
#     icr_list = []
#     if current_response.is_correct == True:
#         cr_list.append(current_response)
#         print ("this is correct list", cr_list)
#     else:
#         icr_list.append(current_response)
#         print ("this is ic list", icr_list)

#     context = { "current_level": current_response.levels}
#     return render( request, 'student/report.html', context)

# def

#     context = {"current_level": current_level}

#     return render(request, 'student/report.html', context)
def question_level(request):
    user=user
    questions = Question.objects.all().filter(question=question, user=user)
    responses = Responses.objects.all().filter(user=user).order_by(-"submitted")

    last_repsonse = responses[0]


def get_current_level(request):
    user = request.user
    question = Question.objects.all().filter(user=user).order_by("-submitted")
    current_question= question[0]
    current_level= current_question.level
    print ("views2 running")

    context = {"current_level": current_level,}

    return render(request, 'student/report.html', context)


def question_detail(request, question_id):
    user=request.user 
    question= Question.objects.get(pk=question_id)
    responses= Response.objects.all().filter(question=question, user=user)
    attempts= len(responses)
    unique = unique_responses(responses)


    context = { "question": question, "responses": unique, "attempts": attempts}

    return render ( request, 'student/question_detail.html', context)

def response_type(request):
    questions = Question.objects.all(user=user)
    responses = Response.objects.all(question=quesiton,user=user)


def unique_responses(responses):
    unique_responses=[]
    for r in responses:
        if r.code not in unique_responses:
            unique_responses.append(r.code_pp())
    return unique_responses

def study_sessions(user):

    responses = Response.objects.filter(user=user).order_by("-submitted")
    study_sessions = []
    qid = responses[0].question.id
    attempts = []
    for r in responses:
        # print("question id: {}".format(r.question.id))

        if r.question.id != qid:
            print("*** creating new session --------------")
            study_sessions.append(StudySession(attempts))
            attempts = []
            qid = r.question.id
        
        attempts.append(r)
    
    study_sessions.append(StudySession(attempts))

    context={"study_sessions": study_sessions,}

    return render( request, 'student_report', context)

    # session = total responses for single question in a continuous block of time
    # WE ARE returning the single session for the latest question

class StudySession(object):

    def __init__(self, responses):

        assert len(responses) > 0

        self.question = responses[0].question
        print(responses)
        print(type(responses))
        self.level= responses[0].question.level
        self.session_start = responses[0].submitted
        self.session_end = responses[-1].submitted
        self.time_elapsed = self.session_end - self.session_start
        self.num_correct = len([r for r in responses if r.is_correct==True])
        self.num_wrong = len(responses) - self.num_correct
        self.responses = responses


        




