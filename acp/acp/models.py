from django.db import models
from django.conf import settings
import os

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
    
    COLOR_OPTIONS = (
                     ('b', 'blue'),
                     ('g', 'green'), 
                     ('r', 'red'), 
                     ('c', 'cyan'), 
                     ('m', 'magenta'), 
                     ('y', 'yellow'), 
                     ('k', 'black'), 
                    )
    
    color = models.CharField(max_length=64, default='k', choices=COLOR_OPTIONS)
    
    MARK_OPTIONS = (
                    ('.', 'point'),
                    (',', 'pixel'),
                    ('o', 'circle'),
                    ('v', 'triangle_down'),
                    ('^', 'triangle_up'),
                    ('<', 'triangle_left'),
                    ('>', 'triangle_right'),
                    ('8', 'octagon'),
                    ('s', 'square'),
                    ('p', 'pentagon'),
                    ('*', 'star'),
                    ('h', 'hexagon1'),
                    ('H', 'hexagon2'),
                    ('+', 'plus'),
                    ('x', 'x'),
                    ('D', 'diamond'),
                    ('d', 'thin_diamond'),
                    ('|', 'vline'),
                    ('_', 'hline'),
                    ('TICKLEFT', 'tickleft'),
                    ('TICKRIGHT', 'tickright'),
                    ('TICKUP', 'tickup'),
                    ('TICKDOWN', 'tickdown'),
                    ('CARETLEFT', 'caretleft'),
                    ('CARETRIGHT', 'caretright'),
                    ('CARETUP', 'caretup'),
                    ('CARETDOWN', 'caretdown'),
                )
    
    mark = models.CharField(max_length=64, default='o', choices=MARK_OPTIONS)
    labels = models.BooleanField(default=False)

class Document(models.Model):
    """ Specific document metadata reference.  The actual document is stored 
    remotely.  """
    name = models.CharField(max_length=64)
    corpus = models.ForeignKey('Corpus')
    category = models.ForeignKey('Category')
    file = models.FileField(default=None, blank=True)

    # Clean up file when model is deleted
    def delete(self,*args,**kwargs):
        self.file.delete()
        super(Document, self).delete(*args,**kwargs)

class Visual(models.Model):
    """ Stores meta data about visuals created for corpa """
    corpus = models.ForeignKey('Corpus')
    file = models.ImageField(default=None, blank=True)
    
    def delete(self,*args,**kwargs):
        self.file.delete()
        super(Visual, self).delete(*args,**kwargs)    