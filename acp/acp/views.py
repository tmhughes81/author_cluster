from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout


def index(request):
    args = {}
    return render(request, "index.html", args)

def dashboard(request):
    args = {}
    return render(request, "index.html", args)
    
def logout_view(request):
    args = {}
    logout(request)
    
    return render(request, "index.html", args)

    