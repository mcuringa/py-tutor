import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserChangeForm

from social.models import *

def profile(request):

    return render(request, 'social/profile.html')

def public(request, username):
    profile = SocialProfile.objects.get(user__username=username)
    cx = {"username":username, "profile":profile}

    return render(request, 'social/public.html', cx)

def find_friends(request):
    q = request.GET["q"]
    results = RestProfile.objects.filter(user__username__startswith=q)

    if len(results) == 0:
        return HttpResponse("[]", content_type="application/json")

    j_results = [r.as_json() for r in results]

    data = ",".join(j_results)
    data = "[" + data + "]"
    print(data)

    return HttpResponse(data, content_type="application/json")


def post_profile_pic(request):
    if request.method == 'POST':
        profile = RestProfile.objects.get(user__username=request.user.username)
        form = SocialProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


class ConnectionView(View):

    def get(self, request):
        
        user = request.user
        friends = FriendConnection.objects.all(friend_a=user.username)

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
                print(form.instance)
                print(form.instance.user)
                print(form.user)
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

    
