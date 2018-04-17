from django import forms
from mainApp.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title','description', 'image', ]

    def save(self, force_insert=False,force_update=False, commit=True):
    	image=super(ImageForm,self).save(commit=False)

    	if commit:
    		image.save()
    	return image

class SignupForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = Member
		fields = ("username","password",)
