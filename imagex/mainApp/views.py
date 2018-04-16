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
from django.contrib.auth import login, authenticate
from django.template import loader
from django.contrib.auth.models import User
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from mainApp.models import *
from mainApp.forms import ImageForm
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


MAX_NUMBER=100
MAX_FREQUENCY=100
TAG_LIMIT = 10


def home(request):
    return HttpResponse("This is main app")

#login 
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect(upload)
        else:
            return render(request,'login.html', {'feedback':json.dumps("Please input correct username and password!")})   
    return render(request,'login.html')

# Upload view
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
            new_item.save()   
            if not Category.objects.filter(name=category):
                new_category = Category(name=category)
                new_category.save()   
            new_item.category = Category.objects.get(name=category)          
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

def search_by_photographer(request):
	if request.method=='GET':
		photographer_name= request.GET.get('keyword')

	try:
		photographer_id= Member.objects.get(username=keyword)
	except ObjectDoesNotExist:
		photographer_id=None

	result_images= Image.model.filter(owner=photographer_id)

	context={
		'result_images': result_images
	}
	return render(request, 'search.html', context)

def search_by_category(request):
	if request.method=='GET':
		galler_name= request.GET.get('keyword')

	try:
		gallery_id= Gallery.objects.get(name=keyword)
	except ObjectDoesNotExist:
		gallery_id=None

	result_images= Gallery.model.filter(gallery= gallery_id)

	context={
		'result_images': result_images
	}
	return render(request, 'search.html', context)


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
