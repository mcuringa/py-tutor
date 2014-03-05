from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tutor.models import *


def study(request):
    """Choose the next question for the user to study."""
    return render(request, 'tutor/study.html')


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
        tests = []
    else:
        question = Question.objects.get(pk=pk)
        form = QuestionForm(instance=question)
        history = ArchiveQuestion.objects.all().filter(parent_id=pk)
        tests = Test.objects.all().filter(question=question)


    test_form = TestForm()

    context = { "question": form,
                "pk": pk,
                "history": history,
                "test_form": test_form,
                "tests": tests
              }

    return render(request, 'tutor/question_form.html', context)

@login_required
def save_question(request):

    pk = int(request.POST["pk"])
    if pk > 0:
        q = Question.objects.get(pk=pk)
        form = QuestionForm(request.POST, instance=q)
        aq = ArchiveQuestion()
        aq.archive(form.instance)
        aq.modifier = request.user
        aq.save()
        form.instance.version += 1
    else:
        form = QuestionForm(request.POST)
        form.instance.version = len(ArchiveQuestion.objects.all()) + 1
        form.instance.creator = request.user

    form.instance.modifier = request.user

    question = form.save()
    return HttpResponseRedirect("/tutor/list")


