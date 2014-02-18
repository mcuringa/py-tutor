from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tutor.models import *


def study(request):
    """Choose the next question for the user to study."""
    return render(request, 'tutor/study.html')


def list(request):
    """List the questions in the databse"""
    
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



