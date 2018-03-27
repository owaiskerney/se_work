from django.shortcuts import render
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
from upload.validators import validate_file_extension
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import login, authenticate
from django.template import loader
from django.contrib.auth.models import User
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from upload.models import *
from upload.forms import ImageForm





def index(request):
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
        description = request.POST.get('description')
        tag_list = tag.split(',')
        for tag in tag_list: 
            if not Tag.objects.filter(name=tag):
                new_tag = Tag(name=tag)
                new_tag.save()

        total = Image.objects.filter(owner=request.user).count()
        frequency = Image.objects.filter(owner=request.user, uploadtime=datetime.date.today()).count()
       
        if form.is_valid() and total < 100 and frequency < 100:
            cd = form.cleaned_data
            new_item=form.save(commit=False)
            new_item.owner = request.user
            new_item.title = title 
            new_item.description = description          
            new_item.save()  
            for item in tag_list:
                new_item.tag.add(Tag.objects.get(name=item))         
            return redirect(home)
        elif not form.is_valid():
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("Please submit JPEG file!")})   
        elif total >= 100:
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You are only allowed to maintain 3 images!")})   
        elif frequency >= 100: 
            form=ImageForm()
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You are only allowed to upload 4 images per day!")})    
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})



# Search view
def search(request):
	#if not isAuthenticated(request):
	#find tag in Tag
	#use tag_id to get corresponding image_id in many to many table
	#keep using image_ids obtained from this query to return all images to front end
	tag_id_found= tag_id in Tag.objects.filter(name= tag)
	

	#if tag not found
	#if (tag_id_found== ):
		#Implement tag not found

	#if tag found, look for corresponding image_id
	image_id_list=[it.image_id for it in Image.Tag.filter(tag_id=tag_id_found)]

	#Connect images to front end to load them
	image_results=[]
	for i in image_id_list:
		image_results.append()



	#return the search.html page with laoded images 



	context={}




	return render(request, 'mainApp/Search.html', context)

	#return redirect('/home')


#tags = Tag.objects.all()
