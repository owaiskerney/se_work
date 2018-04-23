from django import forms
from upload.models import Image, Category
from django.shortcuts import get_object_or_404

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','tag','category', 'description', 'image',)
