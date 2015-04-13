import json
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from django.db.models import Q

from social.models import *
from pytutor import settings

def profile(request):

    return render(request, 'social/profile.html')

def public(request, username):

    friend = User.objects.get(username=username)
    status = get_friend_status(request.user, friend)
    if status == "friend":
        profile = RestProfile.objects.get(user__username=username)
    else:
        profile = PublicRestProfile.objects.get(user__username=username)

    cx = {"profile": profile.as_json(extra={"friend_status": status})}
    print(cx["profile"])

    return render(request, 'social/public.html', cx)



def find_friends(request):
    q = request.GET["q"]
    results = RestProfile.objects.filter(user__username__startswith=q).exclude(user=request.user)

    if len(results) == 0:
        return HttpResponse("[]", content_type="application/json")

    j_results = [r.as_json() for r in results]

    data = ",".join(j_results)
    data = "[" + data + "]"
    print(data)

    return HttpResponse(data, content_type="application/json")


def post_profile_pic(request):
    
    if request.method != 'POST':
        return "This method only supports POST requests."

    profile = RestProfile.objects.get(user__username=request.user.username)
    form = SocialProfileForm(request.POST, request.FILES, instance=profile)
    uploaded = RestProfile(profile_pic=request.FILES['file'])
    profile.profile_pic = uploaded.profile_pic

    profile.save()

    return HttpResponse(profile.as_json(), content_type="application/json")



def get_friend_status(user, friend):
    if not user.is_authenticated():
        return "join"
    
    try:
        friend = FriendConnection.objects.get(friend_a=user, friend_b=friend)
        return "friend"
    except:
        pass

    try:
        friend = FriendRequest.objects.get(sender=user, invited=friend)
        return "pending"
    except:
        pass

    try:
        friend = FriendRequest.objects.get(sender=friend, invited=user)
        return "invited"
    except:
        pass

    return ""

class ConnectionView(View):

    def get(self, request):
        
        user = request.user
        try:
            friends = FriendConnection.objects.get(Q(friend_a=user) | Q(friend_b=user), status="accepted")
        except:
            friends = []

        try:
            sent = FriendConnection.objects.get(Q(friend_a=user), status="pending")
        except:
            sent = []

        try:
            pending = FriendConnection.objects.get(Q(friend_b=user), status="pending")
        except:
            pending = []


        return HttpResponse(profile.as_json(), content_type="application/json")


class SocialView(View):

    def get(self, request):
        user = request.user
        profile = RestProfile.objects.get(user__username=user.username)

        return HttpResponse(profile.as_json(), content_type="application/json")
    
    @method_decorator(csrf_exempt)
    def put(self, request):
        profile = RestProfile.objects.get(user__username=request.user.username)
        # print(request.body.decode("utf-8"))

        form = SocialProfileForm(json.loads(request.body.decode("utf-8")), instance=profile)
        user_form = CustomUserChangeForm(json.loads(request.body.decode("utf-8")))

        try:
            user = request.user
            form.user = user

            if form.is_valid() and user_form.is_valid():
                user.first_name = user_form.cleaned_data["first_name"]
                user.last_name = user_form.cleaned_data["last_name"]
                user.email = user_form.cleaned_data["email"]

                user.save()
                form.save()
            else:
                print("form was not valid")
                print(form.errors.as_data())
        except Exception as ex:
            print("exception while saving...")
            print(ex)
            print(user_form.errors)
            print(form.errors)

        return HttpResponse(profile.as_json(), content_type="application/json")

    @method_decorator(csrf_exempt)
    def post(self, request):
        return self.put(request)

    
