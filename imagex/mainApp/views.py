from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request):
	return HttpResponse("This is main app")


# Upload view
def upload(request):
	if not isAuthenticated(request):
		return redirect('/mainApp/index')


# Search view
def search(request):
	if not isAuthenticated(request):
		return redirect('/mainApp/index')
tags = Tag.objects.all()