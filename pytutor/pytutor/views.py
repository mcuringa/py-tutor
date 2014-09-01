from django.shortcuts import render

def home(request):
    """Home Page Content...static for now."""

    return render(request, 'home.html')

if  __name__ =='__main__':main()