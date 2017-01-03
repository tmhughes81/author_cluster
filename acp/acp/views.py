from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from forms import CreateCorpusForm
from models import Corpus, CorpusOwners
from django.contrib.auth.models import User

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


def create_corpus(request):
    """ Used to create a new corpus """
    if request.POST:
        form = CreateCorpusForm(request.POST)
        if form.is_valid():
            """ First the Corpus object """
            corpus_form = form.save(commit=False)
            
            corpus_form.save()
            
            user = request.user
            
            """ Then the ownership """
            owners = CorpusOwners.create_owners(user=user, corpus=corpus_form)
            owners.save()
    
    return HttpResponseRedirect('/dashboard/')

def del_corpus(request, corpus_id):
    """ Deletes a corpus """
    if not Corpus.objects.filter(id=corpus_id).exists():
        return HttpResponseRedirect('/corpus/not_found/')
    
    Corpus.objects.get(id=corpus_id).delete()
    
    return HttpResponseRedirect('/dashboard/')