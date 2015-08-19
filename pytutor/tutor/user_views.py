from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from social.models import SocialProfile



def register(request):
    
    form = UserCreationForm()

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if len(password) < 3:
            messages.warning(request, 'Could not create account. Your password must be at least 3 chars long.')
            return HttpResponseRedirect('/')

        try:        
            user = User.objects.create_user(username=username, password=password)
            SocialProfile.objects.create(user=user)
            
            user = authenticate(username=username, password=password)
            messages.info(request, "Your account has been created and you are logged in. Welcome to PyTutor.")
            login(request, user)
        except Exception as ex:
            try:
                User.objects.get(username=username)
            except:
                messages.warning(request, 'There was a problem creating your account.')
            messages.warning(request, 'No account created: {} is already in use.'.format(username))
    
    return HttpResponseRedirect('/')

def user_login(request):
    
    if request.method == 'POST':
        if "register" in request.POST:
            return register(request)

        username = request.POST['username']
        password = request.POST['password']          
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, 'You are successfully logged in.')
            return HttpResponseRedirect('/')

        
        return HttpResponseRedirect('/login-sorry')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You are now logged out.')
    return HttpResponseRedirect('/')


def login_error(request):
    """Let the user know that login failed."""

    return render(request, 'login-sorry.html')

