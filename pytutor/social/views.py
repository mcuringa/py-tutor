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
from django.db.models import Count


from django.views.generic import View


from models import *

def profile(response):

    return render(request, 'social/profile.html', context)


class SocialView(View):

    @login_required
    def get(self, request):
        user=request.user
        profile = SocialProfile.objects.get(user=user)

        

        return HttpResponse('result')


    
