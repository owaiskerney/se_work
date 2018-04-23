from django import forms
from mainApp.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError

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
        fields = ("username","email",)

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not Member.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no member registered with this email address, please input again.")
        return email

class EditProfileForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Member
        fields = ['first_name', 'last_name', 'email','avatar','self_description', 'password',]


