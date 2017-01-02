from django import forms
from models import Corpus

class CreateCorpusForm(forms.ModelForm):
    
    class Meta:
        model = Corpus
        fields = ['name', 'public']