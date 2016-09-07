from django import forms

class UploadFileForm(forms.Form):

    file = forms.FileField(required=False, label="", widget=forms.ClearableFileInput(attrs={'value': '{{files}}'}))
