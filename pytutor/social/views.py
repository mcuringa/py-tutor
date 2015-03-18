import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from social.models import *

def profile(request):

    return render(request, 'social/profile.html')


class SocialView(View):

    def get(self, request):
        user = request.user
        profile = RestProfile.objects.get(user__username=user.username)

        return HttpResponse(profile.as_json(), content_type="application/json")
    
    @method_decorator(csrf_exempt)
    def put(self, request):
        profile = RestProfile.objects.get(user__username=request.user.username)
        # print(request.body.decode("utf-8"))

        form = SocialProfileForm(json.loads(request.body.decode("utf-8")))
        form.instance = profile
        try:

            form.user = request.user
            if form.is_valid():
                form.save()
            else:
                print("form was not valid")
                print(form.instance)
                print(form.instance.user)
                print(form.user)
                print(form.errors.as_data())
        except Exception as ex:
            print(ex)
            print(form.errors)

        return HttpResponse(profile.as_json(), content_type="application/json")

    @method_decorator(csrf_exempt)
    def post(self, request):
        return self.put(request)

    
