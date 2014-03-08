from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, HttpResponseRedirect


def register(request):
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Your account is created, welcome to PyTutor.')


            #now, log the user in
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, 'There was a problem creating your account.')
    
    context = {"form": form}

    return render(request, 'register.html', context)

def user_login(request):
    
    if request.method == 'POST':

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

