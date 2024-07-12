# upload/forms.py

from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()
    tag = forms.CharField(max_length=255)