import random
import json
from operator import itemgetter, attrgetter


from django.template import loader, Context
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.db.models import Q

from tutor.models import *
from django.db.models import Count
import tutor.study as sm

@login_required
def report(request):

    user=request.user

# get all of the responses students have made.
# organize them by their level and list their question name.

    student_responses = Response.objects.all().filter(user=user).order_by("question__id")
    
    cur_id = -1 # the current question we're counting up
    rows = []
    data = {}
    right_count = 0
    wrong_count = 0
    # correct_list = []
    # incorrect_list = []

    for r in student_responses:
        q = r.question
        if q.id != cur_id: #start a new row
            # add the data as a row
            data["num_right"] = right_count
            data["num_wrong"] = wrong_count
            data["correct"] = right_count > 0
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

    # find most recently answered question and level
    current_level_number = sm.current_level(user)
    current_level_description = AbstractQuestion.levels[current_level_number - 1]
      

    #get all the levels the student has tried
    level_ids = Response.objects.filter(user=user).order_by("question__level").values_list("question__level").distinct()

    # get list of levels for sidebar
    levels = [(level[0], AbstractQuestion.levels[level[0]-1]) for level in level_ids]


    context = {"student_responses": rows[1:],
                "current_level": current_level_number,
                "current_level_description": current_level_description,
                "levels": levels,
              
               }
    # List questions that student has failed
    return render(request, 'student/report.html', context)






# def say_level_name(request):
#     question = Question.objects.all()

#     for q in question:
#         print (q.level)
#         if q.level == 1:
#             level_name = "Level 1: Basics - simple functions, variables, operators."

#         else:
#             level_name= "not level 1"
#     context = {"question": question,
#                 "level_name": level_name
#                 }
#     return render(request, 'student/report.html', context)


# def get_leveled_questions(request):
#     solved_qs= []
#     unsolved_qs = []
#     user = request.user

#     user_response = Response.objects.all().filter(user=user)

#     for r in user_response:
#         print (r)
#         if r.is_correct:
#             solved_qs.append(r)
#             print (solved_qs)
#         else:
#             unsolved_qs.append(r)
#             print (unsolved_qs)

#     context = {"solved_qs": solved_qs,
#                 "unsolved_qs": unsolved_qs
#                 }
#     return render(request, "student/report.html", context)

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


# def simple(request):
#     user=request.user 
#     res = Response.objects.all()[:3]
#     for r in res:
#         r1 = r[1]
#         print (r1)

#     context = {"r1": r1,
#             }
#     return render(request, 'student/report.html', context)








# def organize_report(request):

#     user = request.user
#     all_responses = Response.objects.all().filter(user=user)
#     all_questions = Question.objects.all()
#     level_questions = Question.objects.by_level()

#     print (level_questions)

#     solved_question = []
#     unsolved_question = []
   
#     for r in all_responses:
#         if r.question.is_correct:
#             print(r.question.is_correct)
#     # for q in all_questions:
#     #     if q.response.is_correct:
#             print ("This is working, while q.resp.is_correct")
#             solved_question.append(r)
#         else:
#             unsolved_question.append(r)
#     print ("this is a solved question", solved_question[1])
    
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
# def question_level(request):
#     user=user
#     questions = Question.objects.all().filter(question=question, user=user)
#     responses = Responses.objects.all().filter(user=user).order_by(-"submitted")

#     last_repsonse = responses[0]


# def get_current_level(request):
#     user = request.user
#     question = Question.objects.all().filter(user=user).order_by("-submitted")
#     current_question= question[0]
#     current_level= current_question.level
#     print ("views2 running")

#     context = {"current_level": current_level,}

#     return render(request, 'student/report.html', context)


def question_detail(request, question_id):
    user=request.user 
    question= Question.objects.get(pk=question_id)
    responses= Response.objects.all().filter(question=question, user=user)
    attempts= len(responses)
    unique = unique_responses(responses)



    context = { "question": question, "responses": unique, "attempts": attempts}
    expert_solutions, user_solutions = solutions(question)
    context["expert_solutions"] = expert_solutions
    context["user_solutions"] = user_solutions
    return render ( request, 'student/question_detail.html', context)

def solutions(question):
    
    tests = Test.objects.filter(question=question)
    user_solutions = Response.objects.filter(question=question, is_correct=True).values_list("code").distinct()
    expert_solutions = sorted(list(set(Solution.objects.filter(parent=question))), key=attrgetter('version'), reverse=True)
    for sol in expert_solutions:
        sol.test(tests)

    user_solutions = [syn(c[0]) for c in user_solutions]

    return expert_solutions, user_solutions

def model_responses(request):
    question = Question.objects.get(pk=pk)


    return render(request, 'tutor/report.html', context)

# @login_required
# def respond(request):
#     """Allow user to write a response to a question."""

#     pk = int(request.POST["qpk"])
#     user_code = request.POST.get('user_code', False)
#     sticky_id = int(request.POST.get('sticky_id,', 0))

#     study_tag = request.POST.get('study_tag', False)
#     question = Question.objects.get(pk=pk)  

#     passed, test_results = question.run_tests(user_code)

#     attempts, attempts_left = get_attempts(request.user, question)
#     attempt = len(attempts) + 1
#     attempts_left -= 1
    
#     response = Response(attempt=attempt, user=request.user, question=question)
#     response.code = user_code
#     response.is_correct = passed
#     response.save()

#     context = {"question" : question, 
#                "response" : response, 
#                "attempts_left" : attempts_left,
#                "tests" : test_results,
#                "passed" : passed,
#                "sticky_id": sticky_id,
#                "study_tag": study_tag }
#     if passed or attempts_left % 10 == 0:
#         expert_solutions, user_solutions = solutions(question)
#         context["expert_solutions"] = expert_solutions
#         context["user_solutions"] = user_solutions

#     return render(request, 'tutor/response_result.html', context)


# def response_type(request):
#     questions = Question.objects.all(user=user)
#     responses = Response.objects.all(question=quesiton,user=user)


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


        




