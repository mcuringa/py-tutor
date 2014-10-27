import random
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.db.models import Q

from tutor.models import *

def home(request):
    """Home Page Content...static for now."""

    
    questions = Question.objects.all()
    tags = []

    for question in questions:
        qtags = question.tags.split(",")
        qtags = [q.strip() for q in qtags]
        tags.extend(qtags)

    tags = set(tags)
    tags = sorted([t for t in tags])
    context = {"tags": tags}
    

    return render(request, 'home.html', context)

if  __name__ =='__main__':main()