from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from datetime import datetime, timedelta, date
from django.core.validators import validate_email
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from mainApp.validators import validate_file_extension
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.template import loader
from django.contrib.auth.models import User
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from mainApp.models import *
from mainApp.forms import *
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
import random
from django.core.mail import EmailMessage


MAX_NUMBER=100
MAX_FREQUENCY=100
TAG_LIMIT = 10


def home(request):
    return HttpResponse("This is main app")

#login 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(myaccount)
        else:
            return render(request,'login.html', {'feedback':json.dumps("Please input correct username and password!")})   
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        tokenCode = request.POST.get('token')
        memberEmail = '#'
        if form.is_valid():
            memberEmail = form.cleaned_data.get('email')
            tokens = Token.objects.filter(tokenCode=tokenCode)            
            token_available = False
            for token in tokens:
                if token.email == memberEmail:
                    token_available = True

            if token_available == False:
                return HttpResponse ("Unavailable token!")
            else: 
                form.save()
                return redirect(login_view)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect(search)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(myaccount)
        else: 
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html',{'form':form})

@login_required
def upload(request):
    if request.method == 'POST':
        form= ImageForm(request.POST, request.FILES)
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        category = request.POST.get('category')
        description = request.POST.get('description')
        tag_list = tag.split(',')
        if len(tag_list) > TAG_LIMIT:
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You have reached tag limit!")})               
        total = Image.objects.filter(owner=request.user).count()
        frequency = Image.objects.filter(owner=request.user, uploadtime=datetime.date.today()).count()
       
        if form.is_valid() and total < MAX_NUMBER and frequency < MAX_FREQUENCY:
            cd = form.cleaned_data
            new_item=form.save(commit=False)
            new_item.owner = request.user
            new_item.title = title 
            new_item.description = description          
             
            if not Category.objects.filter(name=category):
                new_category = Category(name=category)
                new_category.save()   
            new_item.category = Category.objects.get(name=category)          
            new_item.save()  
            for tag in tag_list: 
                if not Tag.objects.filter(name=tag):
                    new_tag = Tag(name=tag)
                    new_tag.save() 
            for item in tag_list:
                new_item.tag.add(Tag.objects.get(name=item))         
            return redirect(myaccount)
        elif not form.is_valid():
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("Please submit JPEG file!")})   
        elif total >= MAX_NUMBER:
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You are only allowed to maintain 3 images!")})   
        elif frequency >= MAX_FREQUENCY: 
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You are only allowed to upload 4 images per day!")})    
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})

#search view
def search (request):
    # Extracting keyword to be matched to tag
    if request.method == 'GET':
       keyword = request.GET.get('keyword')
    # Finding tag id of tag supplied as keyword
    try:
        tag_id_found = Tag.objects.get(name=str(keyword))
    except ObjectDoesNotExist:
        tag_id_found = None

    # Finding corresponding image with specified tag   
    result_images = Image.objects.filter(tag=tag_id_found)
    
    context={
      'result_images': result_images
    }     
    return render(request, 'search.html', context)

@login_required
def myaccount(request):
    try:
        image_found = Image.objects.filter(owner=request.user)
    except ObjectDoesNotExist:
        image_found = None
    # Finding corresponding image with specified tag 
    context={
      'image_found': image_found
    }  
    
    return render(request, 'myaccount.html', context)

@login_required
def delete(request,img_pk):
    try:
        results_image = Image.objects.filter(id=img_pk,owner=request.user)
    except:
        results_image = None
    if results_image: 
        results_image.delete()
        return redirect(myaccount)
    else:
        return HttpResponse("You are not allowed to delete it!")
    context={
      'results_image': results_image
    }   
    return render(request, 'myaccount.html',context)

@login_required
def invite(request):
    if request.method == 'GET':
        email = request.GET.get('invite_email')
        if email:
            tokenCode = random.randint(100000,999999)
            Token.objects.create(email = email, tokenCode = tokenCode).save()
            email_body = 'Your invitation token is ' + str(tokenCode)
            sentEmail = EmailMessage ('Invitation from imageX', email_body, to=[email])
            sentEmail.send()
            return redirect(invite_done)
    else: 
        return HttpResponse("Error")
    return render(request, 'invite.html')

@login_required
def invite_done(request):
    return render(request,'invite_done.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(myaccount)
    else: 
        form = EditProfileForm(instance=request.user)
    return render(request,'edit_profile.html',{'form':form})