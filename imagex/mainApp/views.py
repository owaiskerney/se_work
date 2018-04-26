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
from django.contrib.auth.views import PasswordResetView
from operator import attrgetter
from django.http import JsonResponse
from django.http import HttpResponseRedirect



LAST_SEARCH_KEYWORD=""
LAST_SEARCH_KEYWORD_TYPE=""
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
        total = Image.check_upload_limit(request.user)
        frequency = Image.check_frequency_limit(request.user, datetime.date.today())
       
        if (form.is_valid() and total < MAX_NUMBER and frequency < MAX_FREQUENCY):
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
    global LAST_SEARCH_KEYWORD
    global LAST_SEARCH_KEYWORD_TYPE
    
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        category_name = request.GET.get('category')
        sort_by= request.GET.get('sort_by')
        like_image= request.GET.get("like_image")


        photographers=request.GET.get('photographers')
        if (str(photographers) == "True"):
            photographer_name=LAST_SEARCH_KEYWORD
        else:
            photographer_name= ""
        
        if(keyword== None and LAST_SEARCH_KEYWORD !="" and category_name==None and photographers==None and (sort_by!= None or like_image != None) and LAST_SEARCH_KEYWORD_TYPE=="Tag"):
            keyword=LAST_SEARCH_KEYWORD
        elif(keyword== None and LAST_SEARCH_KEYWORD !="" and category_name==None and photographers==None and LAST_SEARCH_KEYWORD_TYPE=="Photographer"and (sort_by!= None or like_image!= None)):
            photographer_name=LAST_SEARCH_KEYWORD
        elif(keyword== None and category_name==None and photographers==None and LAST_SEARCH_KEYWORD_TYPE=="Category" and (sort_by!= None or like_image!=None)):
            print("HOREYAAAAAAAAAAA HAI")
            category_name=LAST_SEARCH_KEYWORD
        elif(keyword==None and category_name!= None):
            LAST_SEARCH_KEYWORD=""
            LAST_SEARCH_KEYWORD_TYPE=""
        elif(keyword != None and LAST_SEARCH_KEYWORD==""):
            LAST_SEARCH_KEYWORD=str(keyword)
        elif(keyword!=None and LAST_SEARCH_KEYWORD!=""):
            LAST_SEARCH_KEYWORD=str(keyword)

        
    # Finding tag id of tag supplied as keyword
    result_images=[]
    if(category_name != None and keyword== None and photographers== None):
        LAST_SEARCH_KEYWORD= category_name
        LAST_SEARCH_KEYWORD_TYPE= "Category"
        try:
            #cat_id_found = Category.objects.get(name=str(category_name))
            cat_id_found = Category.find_cat_id(category_name)
        except ObjectDoesNotExist:
            cat_id_found = None

    # Finding corresponding image with specified tag   
        if (cat_id_found!= None):

            #result_images = Image.objects.filter(category=cat_id_found)
            result_images = Image.retrieve_image_category(cat_id_found)
            print("HOOTIYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            
            print(".............................................................")
            print(".............................................................")
            print(cat_id_found)
            print(".............................................................")
            print(".............................................................")

        

        #Sorting images by recency as default
            result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
    
        context={
        'result_images': result_images
        } 
        #return JsonResponse({'result_images': list(result_images)})
        


    elif (keyword!= None and category_name== None and photographers==None):
        LAST_SEARCH_KEYWORD_TYPE= "Tag"

        keyword_list = keyword.split(' ')

        if(len(keyword_list)==1):

            try:
                tag_id_found = Tag.objects.get(name=str(keyword))
            except ObjectDoesNotExist:
                tag_id_found = None

    
    # Finding corresponding image with specified tag
            if(tag_id_found != None):
                print(".............................................................")
                print(".............................................................")
                print(".............................................................")
                print(tag_id_found)
                print(".............................................................")
                print(".............................................................")
                print(".............................................................")
           
                result_images = Image.objects.filter(tag=tag_id_found)

    #Sorting images by recency as default
                if(sort_by==None or str(sort_by)=="recency"):
                    result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
                else:
                    result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)
                context={
                'result_images': result_images
                }
        else:
            
            all_images= Image.objects.all()
            result_images=[]
            for key in keyword_list:
                
                try:
                    tag_id_found = Tag.search_tag(key)
                except ObjectDoesNotExist:
                    tag_id_found = None

                if (tag_id_found== None):
                    print(".............................................................")
                    print(".............................................................")

                    context={
                        'result_images': result_images
                    }     
                    return render(request, 'search.html', context)
                else:
                    print("ELSAAAAA")
            helper=0
            for image in all_images:
                
                for tags in keyword_list:
                    tag_id_found = Tag.search_tag(tags)
                    founder= Image.image_has_tag(image.id,tag_id_found)
                    if (len(founder)==0):
                        
                        helper=1
                        break
                if(helper==0):        
                    result_images.append(image)
                    
                else:
                    helper=0       


            if(sort_by==None or str(sort_by)=="recency"):
                print("GANDAAAAAAAAAAAAAA")
                result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
            else:
                result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)
            context={
                'result_images': result_images
            }

   			    #result_images = Image.objects.filter(tag=tag_id_found)
            
                    




        #return JsonResponse({'result_images': list(result_images)})
    elif( keyword== None and category_name== None and photographer_name!= ""):
        LAST_SEARCH_KEYWORD_TYPE= "Photographer"
        try:
            #photographer_id_found = Member.objects.get(username=str(photographer_name))
            photographer_id_found= Member.find_member(photographer_name)
        except ObjectDoesNotExist:
            photographer_id_found = None


        print(".............................................................")
        print(".............................................................")
        print(".............................................................")
        print(photographer_name)
        print(".............................................................")
        print(".............................................................")
        print(".............................................................")
    # Finding corresponding image with specified tag   
        result_images = Image.retrieve_image_member(photographer_id_found)

        if(str(sort_by)== "recency"):
            print(".............................................................")
            print(".............................................................")
            print(".............................................................")
            print(photographer_name)
            print(".............................................................")
            print(".............................................................")
            print(".............................................................")
            result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
        elif(str(sort_by)== "popularity"):
            result_images=sorted(result_images, key=attrgetter('popularity'))


    
        context={
            'result_images': result_images
        }    


    
    context={
        'result_images': result_images
    }     
    return render(request, 'search.html', context)
    

#search view
def search_category (request):
    # Extracting keyword to be matched to tag
    if request.method == 'GET':
        category_name = request.GET.get('category')
   
    try:
        cat_id_found = Category.objects.get(name=str(category_name))
    except ObjectDoesNotExist:
        cat_id_found = None
    
    # Finding corresponding image with specified tag   
    if (cat_id_found!= None):

        result_images = Image.objects.filter(category=cat_id_found)

        #Sorting images by recency as default
        result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
    else:
        result_images=[]

    
    context={
        'result_images': result_images
    }     
    return render(request, 'search.html', context)

def search_photographer(request):
    global LAST_SEARCH_KEYWORD
    if request.method == 'GET':
        photographer_name = LAST_SEARCH_KEYWORD
        sort_by= request.GET.get('sort_by')
        
    # Finding tag id of tag supplied as keyword
    
    try:
        photographer_id_found = Member.objects.get(username=str(photographer_name))
    except ObjectDoesNotExist:
        photographer_id_found = None

    # Finding corresponding image with specified tag   
    result_images = Image.objects.filter(owner=photographer_id_found)

    if(str(sort_by)== "recency"):
        
        result_images=sorted(result_images, key=attrgetter('uploadtime'),reverse=True)
    elif(str(sort_by)== "popularity"):
        print(".............................................................")
        print(".............................................................")
        print(".............................................................")
        print(photographer_name)
        print(".............................................................")
        print(".............................................................")
        print(".............................................................")
        result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)


    
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


def browse_by_popularity(request):
    if request.method == 'GET':
        browse_by_popularity = request.GET.get('browse_popularity')

    # Finding tag id of tag supplied as keyword
    result_images=[]
    if(browse_by_popularity == "True"):

    # Finding corresponding image with specified tag   
        result_images = Image.objects.all()
        result_images=sorted(result_images, key=attrgetter('popularity'))
    
    context={
        'result_images': result_images
    }     
    return render(request, 'search.html', context)

def browse_by_popularity_homepage(request):
    if request.method == 'GET':
        browse_by_popularity = request.GET.get('browse_popularity')

    # Finding tag id of tag supplied as keyword
    result_images=[]
    if(browse_by_popularity == None):

    # Finding corresponding image with specified tag   
        result_images = Image.objects.all()
        result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)
    
    context={
        'result_images': result_images
    }     
    return render(request, 'homepage.html', context)

@login_required
def like_images(request):
    if request.method == 'GET':
        like_image= request.GET.get("like_image")
    liked=False
    #img= Image.objects.filter(id=like_image)
    img= Image.get_image(like_image)
    for result in img:
        if (result.owner == request.user):
            print("I own it")
        else:
            try:
                #already_liked = Image.objects.filter(id=like_image,likeby=request.user)
                already_liked = Image.check_already_liked(like_image,request.user)
                print("hahahha")
                # for liker in already_liked:
                #     if (liker== request.user):
                #         liked= True

            except:
                already_liked= ""
            
            if(len(already_liked) == 0):
                print("HAHAHAHAHHAHAAH")
                result.like_stats= result.like_stats+1
               
                mem= Member.objects.filter(id=request.user.id)
            
                for member in mem:
                	result.likeby.add(member)

                #result.likeby.add(Member.objects.get(id=request.user)) 
                result.save()
            else:
                print("You have already liked this photo")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def download_images(request,img_pk):
    try: 
        results_image = Image.objects.get(id=img_pk)
    except:
        results_image = None    
    if results_image:
        results_image.download_stats=results_image.download_stats+1
        results_image.save()
        print(results_image.download_stats)
        response = HttpResponse(results_image.image, content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename=%s.jpg' % results_image.title
        return response
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def othersaccount(request,member_pk):
    member_id_found = Member.find_member(member_pk)
    result_images = Image.retrieve_image_member(member_id_found)
    context={
        'result_images': result_images,'member_id':member_id_found
    }     
    return render(request, 'othersaccount.html', context)

