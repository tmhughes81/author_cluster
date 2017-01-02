from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from forms import CreateCorpusForm
from models import Corpus


def index(request):
    args = {}
    return render(request, "index.html", args)

def dashboard(request):

    args = {}
    
    corpa = Corpus.objects.all()
    
    args.update({'corpa': corpa})
    
    form = CreateCorpusForm()
    
    args.update({'form': form})
        
    return render(request, "dashboard.html", args)
    
def logout_view(request):
    args = {}
    logout(request)
    
    return render(request, "index.html", args)

def faq(request):
    args = {}
    
    return render(request, "faq.html", args)


def corpus(request):
    if request.POST:
        form = CreateCorpusForm(request.POST)
        if form.is_valid():
            # Using 'fcourse' variable to add the current user to the data.
            corpus_form = form.save(commit=False)
            
            corpus_form.save()
    
    return HttpResponseRedirect('/dashboard/')