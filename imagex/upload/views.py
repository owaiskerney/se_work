from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from upload.models import Image, Member
from upload.forms import ImageForm
from django.http import HttpResponse
from upload.validators import validate_file_extension
import datetime


def home(request):
    images = Image.objects.all()
    return render(request, 'home.html', { 'images': images })

def upload(request,member_id):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        total = Image.objects.filter(owner=member_id).count()
        frequency = Image.objects.filter(owner=member_id, uploadtime=datetime.date.today()).count()
        if form.is_valid() and total < 3 and frequency < 4:
            form.save()
            return redirect(home)
        elif not form.is_valid():
            return HttpResponse('We only support JPEG format!')     
        elif total >= 3:
            return HttpResponse('You are only allowed to maintain 3 images!')    
        elif frequency >= 4: 
            return HttpResponse('You are only allowed to upload 4 images per day!')   
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})