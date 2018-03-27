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




def index(request):
	return HttpResponse("This is main app")


# Upload view
def upload(request):
	#if not isAuthenticated(request):
	return redirect('/home')


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