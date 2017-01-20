from django import forms
from models import Corpus, Document, Category
from sre_constants import CATEGORY

class CreateCorpusForm(forms.ModelForm):
    
    class Meta:
        model = Corpus
        fields = ['name', 'public']

class AddDocForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    file = forms.FileField()
    
    class Meta:
        model = Document
        fields = ['name', 'file']
        
class AddCatForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name', 'mark', 'color']