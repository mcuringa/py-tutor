import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from tutor.models import *

@login_required
def study(request):
    """Randomly choose the next question for the user to study.
       If no questions exist, prompt the user to create one."""

    try:
    	question = random.choice(Question.objects.all())
    	context = {"question": question}
    	return render(request, 'tutor/study.html', context)
    except: 
        return HttpResponseRedirect("/tutor/no_questions")

@login_required
def no_questions(request):
	return render(request, 'tutor/no_questions.html')

@login_required
def respond(request, pk):
    """Allow user to write a response to a question."""
    
    #responses are linked to ArchiveQuestions, but we're given a Question key
    question = most_recent_version(Question.objects.get(pk=pk))
    
    #if the user has already attempted the question, use existing response object
    try:
    	response = Response.objects.get(user=request.user, question=question)
    #if not, create one
    except: 
    	response = Response(attempt=1, user=request.user, question=question)
    	response.save() #is this necessary here?
    response_form = ResponseForm()
    context = {"question": question, "response" : response, "response_form" : response_form}
    
    return render(request, 'tutor/respond.html', context)

@login_required
def submit_response(request, qpk, rpk):
	"""Submit user's response for evaluation."""
	
	question = Question.objects.get(pk=qpk)
	response = Response.objects.get(pk=rpk)
	context = {"question" : question, "response" : response}
	#needs form stuff too?
	return render(request, 'tutor/feedback.html', context)

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
        form.instance.version += 1
    else:
        form = QuestionForm(request.POST)
        form.instance.version = 1
        form.instance.creator = request.user

    form.instance.modifier = request.user
    question = form.save()
    archive(question)
    
    return HttpResponseRedirect("/tutor/list")


def archive(question):
    aq = ArchiveQuestion()
    aq.archive(question)
    aq.modifier = question.modifier
    aq.save()
    
def most_recent_version(question):
	all = ArchiveQuestion.objects.all().filter(parent_id=question.pk)
	most_recent = all[0]
	for q in all:
		if most_recent.modified < q.modified:
			most_recent = q
	return most_recent
	
