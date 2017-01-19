from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from forms import CreateCorpusForm, AddDocForm, AddCatForm
from models import Corpus, CorpusOwners, Category, Document
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


def corpus(request, corpus_id):

    args = {}
    
    corpus = Corpus.objects.get(id=corpus_id)
    
    args.update({'corpus': corpus})
    
    categories = Category.objects.filter(corpus=corpus)
    
    args.update({'categories': categories})
    
    documents = Document.objects.filter(corpus=corpus)
    
    args.update({'documents': documents})
    
    cat_form = AddCatForm()
    args.update({'cat_form': cat_form})
    
    doc_form = AddDocForm()
    
    args.update({'doc_form': doc_form})
    
    return render(request, "corpus.html", args)
    
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

def add_doc(request, corpus_id):
    if request.POST:
        form = AddDocForm(request.POST, request.FILES)
        if form.is_valid():
            """ First the Corpus object """
            doc = form.save(commit=False)
            
            doc.corpus = Corpus.objects.get(id=corpus_id)
            doc.category = Category.objects.get(name=request.POST['category'])
            doc.save()
    else:
        HttpResponseRedirect('/')
    
    url = '/corpus/'+corpus_id
    
    return HttpResponseRedirect(url)

def add_cat(request, corpus_id):
    if request.POST:
        form = AddCatForm(request.POST)
        if form.is_valid():
            cat_form = form.save(commit=False)
            cat_form.corpus = Corpus.objects.get(id=corpus_id)
            cat_form.save()
    else:
        HttpResponseRedirect('/')
    
    url = '/corpus/'+corpus_id
    
    return HttpResponseRedirect(url)

def del_doc(request, doc_id):
    """ Deletes a document """
    if not Document.objects.filter(id=doc_id).exists():
        return HttpResponseRedirect('/corpus/not_found/')
    
    doc = Document.objects.get(id=doc_id)
    doc.delete()
    
    return HttpResponseRedirect('/dashboard/')

def del_cat(request, cat_id):
    """ Deletes a category """
    if not Category.objects.filter(id=cat_id).exists():
        return HttpResponseRedirect('/corpus/not_found/')
    
    Category.objects.get(id=cat_id).delete()
    
    return HttpResponseRedirect('/dashboard/')