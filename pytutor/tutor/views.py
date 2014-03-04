import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tutor.models import *


def study(request):
    """Choose the next question for the user to study."""
    
    question = random.choice(Question.objects.all())
    context = {"question": question}
    return render(request, 'tutor/study.html', context)

def respond(request, pk):
    """Allow user to write a response to a question."""
    
    pk = int(request.GET["pk"])
    question = Question.objects.get(pk=pk)
    context = {"question": question}
    
    return render(request, 'tutor/respond.html', context)

def submit_response(request, qpk, rpk):
	"""Submit user's response for evaluation."""
	
	question = Question.objects.get(pk=qpk)
	response = Response.objects.get(pk=rpk)
	context = {"question" : question, "response" : response}
	#needs form stuff too
	return render(request, 'tutor/feedback.html', context)

def list(request):
    """List the questions in the database"""
    
    questions = Question.objects.all()
    context = {"questions": questions}
    
    return render(request, 'tutor/list.html', context)

def new_question(request, pk=0):
    
    if pk == 0:
        form = QuestionForm()
    else:
        print("editing an existing app with primary key", pk)
        question = Question.objects.get(pk=pk)
        form = QuestionForm(instance=question)

    context = { "question": form, "pk": pk }

    return render(request, 'tutor/question_form.html', context)

def save_question(request):

    pk = int(request.POST["pk"])
    if pk > 0:
        q = Question.objects.get(pk=pk)
        form = QuestionForm(request.POST, instance=q)
    else:
        form = QuestionForm(request.POST)

    question = form.save()
    return HttpResponseRedirect("/tutor/list")



