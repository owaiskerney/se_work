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
from .functions import *



def index(request):
	return HttpResponse("This is main app")


# Upload view
def upload(request):
	#if not isAuthenticated(request):
	return redirect('/index')


# Search view
def search(request):
	#if not isAuthenticated(request):
	return redirect('/index')


#tags = Tag.objects.all()