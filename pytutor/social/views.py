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
        raise Exception("This method only supports POST requests.")

    profile = RestProfile.objects.get(user__username=request.user.username)
    form = SocialProfileForm(request.POST, request.FILES, instance=profile)
    uploaded = RestProfile(profile_pic=request.FILES['file'])
    profile.profile_pic = uploaded.profile_pic

    profile.save()

    return HttpResponse(profile.as_json(), content_type="application/json")


def add_friend_request(request):
    if request.method != 'POST':
        raise Exception("This method only supports POST requests.")

    sender = request.user

    friend = request.POST["username"]
    invited = User.objects.get(username=friend)
    
    if FriendRequest.objects.filter(sender=sender, invited=invited).count() > 0:
        return HttpResponse(json.dumps({"msg":"friend relationship already exists."}), content_type="application/json")

    FriendRequest.objects.create(status="pending", sender=request.user, invited=invited)
    return HttpResponse(json.dumps({"msg":"friend request sent."}), content_type="application/json")


def accept_friendship(request):
    if request.method != 'POST':
        raise Exception("This method only supports POST requests.")

    sender = User.objects.get(username=request.POST["username"])
    invited = request.user

    try:
        fr = FriendRequest.objects.get(sender=sender, invited=invited, status="pending")
    except Exception as ex:
        print(ex)
        return HttpResponse(json.dumps({"msg":"friend request could not be accepted."}), content_type="application/json")    

    fr.status = "accepted"
    fr.save()
    FriendConnection.objects.create(friend_a=sender, friend_b=invited)
    FriendConnection.objects.create(friend_a=invited, friend_b=sender)
    profile = RestProfile.objects.get(user__username=sender.username)

    return HttpResponse(profile.as_json(extra={"friend_status":"friend"}), content_type="application/json")


def get_friend_status(user, friend):
    if not user.is_authenticated():
        return "join"
    
    if FriendConnection.objects.filter(friend_a=user, friend_b=friend).count() > 0:
        return "friend"

    if FriendRequest.objects.filter(sender=user, invited=friend).count() > 0:
        return "pending"

    if FriendRequest.objects.filter(sender=friend, invited=user).count() > 0:
        return "invited"

    if user.username == friend.username:
        return "friend"


    return ""

def social_status(request):
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponse({}, content_type="application/json")

    try:
        pending = FriendRequest.objects.filter(invited=user, status="pending")
    except:
        pending = []

    data = {}
    pending = [f.as_json() for f in pending]
    pending = ",".join(pending)
    pending = "[" + pending + "]"
    data["friend_requests"] = pending

    return HttpResponse(json.dumps(data), content_type="application/json")





class SocialView(View):

    def get(self, request):
        user = request.user
        profile = RestProfile.objects.get(user__username=user.username)
        status = get_friend_status(user, profile.user)

        return HttpResponse(profile.as_json(extra={"friend_satus": status}), content_type="application/json")
    
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

    
