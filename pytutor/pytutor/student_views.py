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
	student_responses=Response.get.all().filter(user=user).order_by("-submitted")

	# student report:
	# check progress,
	# show level
	# show questions studied number
	# show times they study
	# show times they get the highest rates
	#
	#questionlist function / list.html views  # table sortable / data-sort val to tell what to sort on(if differnt from whats in cell)