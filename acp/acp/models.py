from django.db import models
from django.conf import settings

class Corpus(models.Model):
    """ A collection of categories and documents that will be clustered """
    name = models.CharField(max_length=64) # Name of the Corpus
    public = models.BooleanField(default=False)
    cat_count = models.IntegerField(default=0)
    doc_count = models.IntegerField(default=0)

class CorpusOwners(models.Model):
    """ More than one person can own a Corpus; this gives them editing rights """
    corpus = models.ForeignKey('Corpus')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    """ Gets called as part of corpus creation """    
    @classmethod
    def create_owners(cls, user, corpus):
        entry = cls(owner=user, corpus=corpus)
        
        return entry
    

class Category(models.Model):
    """ A sub-category attached to a corpus (often an author) """
    name = models.CharField(max_length=64)
    corpus = models.ForeignKey('Corpus')
    color = models.CharField(max_length=64)
    mark = models.CharField(max_length=64)
    labels = models.BooleanField(default=False)

class Document(models.Model):
    """ Specific document metadata reference.  The actual document is stored 
    remotely.  """
    name = models.CharField(max_length=64)
    corpus = models.ForeignKey('Corpus')
    category = models.ForeignKey('Category')
    uri = models.URLField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    