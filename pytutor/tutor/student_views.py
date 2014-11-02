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


@login_required
def report(request):

	user=request.user
	# student_responses=Response.objects.all().filter(user=user).order_by("-submitted")
	student_responses = Response.objects.all()


# single table w all questions and whether you got it right or wrong.


# group by queries (django) don't do.


# map.. python, functools library.  take a list and apply function to every item and return one thing


	# # List questions that student has passed
	# questions_passed=Response.objects.all().filter(user=user, is_correct=True)
	# questions_failed=HttpResponse.objects.all().filter(user=user, is_correct=False)

	# context = {"questions_passed": questions_passed,
	# 	"questions_failed": questions_failed}

	context = {"student_responses": student_responses}
	# List questions that student has failed
	return render(request, 'student/report.html', context)

	# student report:
	# check progress,
	# show level
	# show questions studied number
	# show times they study
	# show times they get the highest rates
	#
	#questionlist function / list.html views  # table sortable / data-sort val to tell what to sort on(if differnt from whats in cell)