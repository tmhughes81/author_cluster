from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render



def index(request):
    args = {}
    return render(request, "index.html", args)