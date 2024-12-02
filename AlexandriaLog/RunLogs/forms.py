from django import forms
from django.forms import ModelForm
from .models import RunModel

class RunForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    runID = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'ID'}))

    class Meta:
        model = RunModel
        fields = "__all__"