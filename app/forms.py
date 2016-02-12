from django import forms

class UploadFileForms(forms.Form):
	img = forms.FileField()