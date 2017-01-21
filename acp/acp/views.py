from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from forms import CreateCorpusForm, AddDocForm, AddCatForm
from models import Corpus, CorpusOwners, Category, Document, Visual
from django.contrib.auth.models import User
from cluster import create_visual
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError

def index(request):
    args = {}
    return render(request, "index.html", args)

def dashboard(request):
    """ Lists all available corpa to a user """
    args = {}
    
    # First list the public corpa
    try:
        public_corpa = Corpus.objects.filter(public=True)
        args.update({'public_corpa': public_corpa})
    except:
        pass
    
    # Then try the user's corpa; double list public corpa
    try:
        my_corpa_owned = CorpusOwners.objects.filter(owner=request.user)
        args.update({'my_corpa_owned': my_corpa_owned})
    except CorpusOwners.DoesNotExist:
        pass
    
    # Add a form for creating new corpa
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
    
    try:
        visual = Visual.objects.get(corpus=corpus)
        args.update({'visual': visual})
        args.update({'visual_file': 'corpa/'+str(visual.file)})
    except Visual.DoesNotExist:
        pass
    
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
    try:
        corpus = Corpus.objects.get(id=corpus_id)
    except Corpus.DoesNotExist:
        return HttpResponseRedirect('/corpus/not_found/')
    
    # User does not have permission to delete corpa that do not belong to them
    if not CorpusOwners.objects.filter(owner=request.user, corpus=corpus).exists():
        return HttpResponseRedirect('/perm_error/')
    
    
    Corpus.objects.get(id=corpus_id).delete()
    
    return HttpResponseRedirect('/dashboard/')

def add_doc(request, corpus_id):
    try:
        corpus = Corpus.objects.get(id=corpus_id)
    except Corpus.DoesNotExist:
        return HttpResponseRedirect('/corpus/not_found/')
    
    # User does not have permission to delete corpa that do not belong to them
    if not CorpusOwners.objects.filter(owner=request.user, corpus=corpus).exists():
        return HttpResponseRedirect('/perm_error/')
    
    if request.POST:
        form = AddDocForm(request.POST, request.FILES)
        if form.is_valid():
            """ First the Corpus object """
            doc = form.save(commit=False)
            
            doc.corpus = Corpus.objects.get(id=corpus_id)
            doc.category = Category.objects.get(name=request.POST['category'])
            doc.save()
            
            doc.corpus.doc_count = Document.objects.filter(corpus=doc.corpus).count()
            doc.corpus.save()
    else:
        HttpResponseRedirect('/')
    
    url = '/corpus/'+corpus_id
    
    return HttpResponseRedirect(url)

def add_cat(request, corpus_id):
    try:
        corpus = Corpus.objects.get(id=corpus_id)
    except Corpus.DoesNotExist:
        return HttpResponseRedirect('/corpus/not_found/')
    
    # User does not have permission to delete corpa that do not belong to them
    if not CorpusOwners.objects.filter(owner=request.user, corpus=corpus).exists():
        return HttpResponseRedirect('/perm_error/')
    
    if request.POST:
        try:
            instance = Category.objects.get(id=request.POST['id'])
            form = AddCatForm(request.POST, instance=instance)
        except MultiValueDictKeyError:
            form = AddCatForm(request.POST)
        
        if form.is_valid():
            cat_form = form.save(commit=False)
            cat_form.corpus = Corpus.objects.get(id=corpus_id)
            cat_form.save()
            
            cat_form.corpus.cat_count = Document.objects.filter(corpus=cat_form.corpus).count()
            cat_form.corpus.save()
            
    else:
        HttpResponseRedirect('/')
    
    url = '/corpus/'+corpus_id
    
    return HttpResponseRedirect(url)

def del_doc(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
    except:
        return HttpResponseRedirect('/doc/not_found/')
    
    try:
        corpus = Corpus.objects.get(id=doc.corpus.id)
    except Corpus.DoesNotExist:
        return HttpResponseRedirect('/corpus/not_found/')
    
    # User does not have permission to delete corpa that do not belong to them
    if not CorpusOwners.objects.filter(owner=request.user, corpus=corpus).exists():
        return HttpResponseRedirect('/perm_error/')

    
    """ Deletes a document """
    if not Document.objects.filter(id=doc_id).exists():
        return HttpResponseRedirect('/corpus/not_found/')
    
    doc.delete()
    
    # Update the document count
    corpus.doc_count = Document.objects.filter(corpus=corpus).count()
    corpus.save()

    
    return HttpResponseRedirect('/corpus/'+str(corpus.id))

def del_cat(request, cat_id):
    """ Deletes a category """
    try:
        cat = Category.objects.get(id=cat_id)
    except:
        return HttpResponseRedirect('/cat/not_found/')
    
    try:
        corpus = Corpus.objects.get(id=cat.corpus.id)
    except Corpus.DoesNotExist:
        return HttpResponseRedirect('/corpus/not_found/')
    
    # User does not have permission to delete corpa that do not belong to them
    if not CorpusOwners.objects.filter(owner=request.user, corpus=corpus).exists():
        return HttpResponseRedirect('/perm_error/')

    Category.objects.get(id=cat_id).delete()
    
    # Update the category count
    corpus.cat_count = Category.objects.filter(corpus=corpus).count()
    corpus.save()
    
    
    return HttpResponseRedirect('/corpus/'+str(corpus.id))

def visualize(request):
    if not request.POST:
        return HttpResponseRedirect('/visual/not_found/')
    
    args = {}
    
    corpus = Corpus.objects.get(id=request.POST['corpus_id'])
    
    if Document.objects.filter(corpus=corpus).count() < 2:
        return HttpResponseRedirect('/perm_error/')
    
    import threading

    t = threading.Thread(target=create_visual,
                            args=[corpus])
    t.setDaemon(True)
    t.start()
    
    
    
    return HttpResponseRedirect('/corpus/'+str(corpus.id))

def cat(request, cat_id):

    args = {}
    
    this_category = Category.objects.get(id=cat_id)
    
    args.update({'this_category': this_category})
    
    args.update({'corpus': this_category.corpus})
    
    categories = Category.objects.filter(corpus=this_category.corpus)
    
    args.update({'categories': categories})
    
    documents = Document.objects.filter(category=this_category)
    
    args.update({'documents': documents})
    
    cat_form = AddCatForm(instance=this_category)
    args.update({'cat_form': cat_form})
    
    doc_form = AddDocForm()
    
    args.update({'doc_form': doc_form})
    
    return render(request, "cat.html", args)

def perm_error(request):
    args = {}
    
    return render(request, 'perm_error.html', args)