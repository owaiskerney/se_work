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

#login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #check whether the member is registered 
        user = Member.check_member(username,password)
        if user is not None:
            #use Django authentication login
            login(request,user)
            return redirect(myaccount)
        else:
            return render(request,'login.html', {'feedback':json.dumps("Please input correct username and password!")})   
    return render(request,'login.html')

#signup view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        tokenCode = request.POST.get('token')
        memberEmail = '#'
        if form.is_valid():
            #check whether email has been used by existing member
            memberEmail = form.cleaned_data.get('email')
            all_emails= Member.objects.all()
            for ema in all_emails:
                print (ema.email)
                if (ema.email== memberEmail):
                    return render(request,'signup.html', {'form':form, 'feedback':json.dumps("This email has already been used!")})

            
            #check whether token is valid
            token_available=Token.check_token(tokenCode,memberEmail)

            if token_available == False:            
                return render(request,'signup.html', {'form':form, 'feedback':json.dumps("Invalid token!")})
            else: 
                form.save()
                Token.objects.filter(tokenCode=tokenCode,email=memberEmail).delete()
                return redirect(login_view)
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


#logout view
@login_required
def logout_view(request):
    #use Django authentication logout
    logout(request)
    return redirect(search)

#password change view
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
            return HttpResponse("error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html',{'form':form})

#upload view
@login_required
def upload(request):
    if request.method == 'POST':
        form= ImageForm(request.POST, request.FILES)
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        category = request.POST.get('category')
        description = request.POST.get('description')
        tag_list = tag.split(',')
        #check upload limit 
        if len(tag_list) > TAG_LIMIT:
            return render(request,'upload.html', {'form':form, 'feedback':json.dumps("You have reached tag limit!")})               
        #check total number of images the member maintains
        total = Image.check_number_limit(request.user)
        #check frequency: the number of image the member uploads today
        frequency = Image.check_frequency_limit(request.user, datetime.date.today())
       
        if (form.is_valid() and total < MAX_NUMBER and frequency < MAX_FREQUENCY):
            cd = form.cleaned_data
            new_item=form.save(commit=False)
            new_item.owner = request.user
            new_item.title = title 
            new_item.description = description          
            
            #check whether the category exists  
            if not Category.objects.filter(name=category):
                new_category = Category(name=category)
                new_category.save()   
            new_item.category = Category.objects.get(name=category)          
            new_item.save()     

            #check tag list
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
    #importing global variables inside function
    global LAST_SEARCH_KEYWORD
    global LAST_SEARCH_KEYWORD_TYPE
    
    #Extracting variables from GET request
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        category_name = request.GET.get('category')
        sort_by= request.GET.get('sort_by')
        like_image= request.GET.get("like_image")


        photographers=request.GET.get('photographers')
        #Determining current and last search type : for example: search by keyword, category or photographer name
        if (str(photographers) == "True"):
            photographer_name=LAST_SEARCH_KEYWORD
        else:
            photographer_name= ""
        
        if(keyword== None and LAST_SEARCH_KEYWORD !="" and category_name==None and photographers==None and (sort_by!= None or like_image != None) and LAST_SEARCH_KEYWORD_TYPE=="Tag"):
            keyword=LAST_SEARCH_KEYWORD
        elif(keyword== None and LAST_SEARCH_KEYWORD !="" and category_name==None and photographers==None and LAST_SEARCH_KEYWORD_TYPE=="Photographer"and (sort_by!= None or like_image!= None)):
            photographer_name=LAST_SEARCH_KEYWORD
        elif(keyword== None and category_name==None and photographers==None and LAST_SEARCH_KEYWORD_TYPE=="Category" and (sort_by!= None or like_image!=None)):
            category_name=LAST_SEARCH_KEYWORD
        elif(keyword==None and category_name!= None):
            LAST_SEARCH_KEYWORD=""
            LAST_SEARCH_KEYWORD_TYPE=""
        elif(keyword != None and LAST_SEARCH_KEYWORD==""):
            LAST_SEARCH_KEYWORD=str(keyword)
        elif(keyword!=None and LAST_SEARCH_KEYWORD!=""):
            LAST_SEARCH_KEYWORD=str(keyword)

        
    
    result_images=[]
    flag_keyword=[]
    last_remembered=[]
    #If search is search by category
    if(category_name != None and keyword== None and photographers== None):
        LAST_SEARCH_KEYWORD= category_name
        LAST_SEARCH_KEYWORD_TYPE= "Category"
        #Finding specific category id for tag supplied
        try:
            
            cat_id_found = Category.find_cat_id(category_name)
        except ObjectDoesNotExist:
            cat_id_found = None

    #Loading images for supplied category 
        if (cat_id_found!= None):

            
            result_images = Image.retrieve_image_category(cat_id_found)
     

        
  
        

    #if search is search by keyword/keyphrase
    elif (keyword!= None and category_name== None and photographers==None):
        LAST_SEARCH_KEYWORD_TYPE= "Tag"
        flag_keyword=[1,2,3]
        keyword_list = keyword.split(',')
        last_remembered=[]
        last_remembered.append(str(keyword))
        #if search is for single keyword
        if(len(keyword_list)==1):
            flag_keyword=[1,2,3]

            try:
                tag_id_found = Tag.objects.get(name=str(keyword))
            except ObjectDoesNotExist:
                tag_id_found = None

    
    # Finding corresponding image with specified tag
            if(tag_id_found != None):
                result_images = Image.objects.filter(tag=tag_id_found)

        #if search is for keyphrase

        else:
            
            all_images= Image.objects.all()
            result_images=[]
            for key in keyword_list:
                
                try:
                    tag_id_found = Tag.search_tag(key)
                except ObjectDoesNotExist:
                    tag_id_found = None

                if (tag_id_found== None):
                   

                    context={
                        'result_images': result_images
                    }     
                    return render(request, 'search.html', context)
                else:
                    print("")
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


            

   			   
    #if search is by photographer
    elif( keyword== None and category_name== None and photographer_name!= ""):
        LAST_SEARCH_KEYWORD_TYPE= "Photographer"
        last_remembered=[]
        last_remembered.append(photographer_name)
        try:
            
            photographer_id_found= Member.find_member(photographer_name)
        except ObjectDoesNotExist:
            photographer_id_found = None


       
    	#loading relevant images for the specified member   
        result_images = Image.retrieve_image_member(photographer_id_found)


    #Handling sort request by recency or popularity: default being recency as well
    if(sort_by== None or str(sort_by)== "recency"):
           
        result_images=sorted(result_images, key=attrgetter('uploadtime'))
        result_images= reversed(result_images)

    elif(str(sort_by)== "popularity"):
        result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)
    
    context={
        'result_images': result_images,
        'flag_keyword': flag_keyword,
        'last_remembered': last_remembered
    }     
    return render(request, 'search.html', context)
    

#myaccount view 
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

#delete view
@login_required
def delete(request,img_pk):
    try:
        images = Image.get_image(img_pk)
    except:
        images = None
    if images: 
        for results_image in images: 
            #check whether the member owns the image
            if results_image.owner == request.user: 
                results_image.delete()
                return redirect(myaccount)
            else:
                return HttpResponse("You are not allowed to delete it!")
    context={
      'results_image': results_image
    }   
    return render(request, 'myaccount.html',context)

#invite view 
@login_required
def invite(request):
    if request.method == 'GET':
        email = request.GET.get('invite_email')
        #check whehter email is valid 
        if email:
            tokenCode = Token.generate_token(email)
            email_body = 'Hi! You have been invited to join imageX as a member! To register, go to our website and use the token ' + str(tokenCode)
            sentEmail = EmailMessage ('Invitation from imageX', email_body, to=[email])
            sentEmail.send()
            return redirect(invite_done)
    else: 
        return HttpResponse("Error")
    return render(request, 'invite.html')

#invite_done view: notification of successful invitation
@login_required
def invite_done(request):
    return render(request,'invite_done.html')

#edit_profile view
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            #check whether email is used by the existing member
            all_email = Member.objects.all()
            for ema in all_email:
                if request.user.email == ema.email:
                    if(request.user != ema):
                        return render(request,'myaccount.html',{'feedback':json.dumps("This email has been used by someone else!")})
                
            form.save()
            return redirect(myaccount)
    else: 
        form = EditProfileForm(instance=request.user)
    return render(request,'edit_profile.html',{'form':form})

#browse_by_popularity view
def browse_by_popularity(request):
    if request.method == 'GET':
        browse_by_popularity = request.GET.get('browse_popularity')

    #preparing to load images
    result_images=[]
    if(browse_by_popularity == "True"):

    # Finding all images and sorting them
        result_images = Image.objects.all()
        result_images=sorted(result_images, key=attrgetter('popularity'))
    
    context={
        'result_images': result_images
    }     
    return render(request, 'search.html', context)

#browse_by_popularity_homepage view for rendering images on homepage
def browse_by_popularity_homepage(request):
    if request.method == 'GET':
        browse_by_popularity = request.GET.get('browse_popularity')

    #preparing to load images
    result_images=[]
    if(browse_by_popularity == None):

    #loading all images and sorting them   
        result_images = Image.objects.all()
        result_images=sorted(result_images, key=attrgetter('popularity'),reverse=True)
    
    context={
        'result_images': result_images
    }     
    return render(request, 'homepage.html', context)

#like_images view for handling like event
@login_required
def like_images(request):
    if request.method == 'GET':
        like_image= request.GET.get("like_image")
    liked=False
    
    img= Image.get_image(like_image)
    for result in img:
    	#Checking if member owns the image being liked
        if (result.owner == request.user):
            return render(request,'search.html',{'feedback':json.dumps("You cannot like your own photo!")})

        else:
            try:
                
                already_liked = Image.check_already_liked(like_image,request.user)
                
                

            except:
                already_liked= ""
            
            if(len(already_liked) == 0):
                
                result.like_stats= result.like_stats+1
               
                mem= Member.objects.filter(id=request.user.id)
            
                for member in mem:
                	result.likeby.add(member)

                 
                result.save()
            #If member has already liked the concerned photo
            else:
                
                return render(request,'search.html',{'feedback':json.dumps("You have already liked this photo!")})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#downloaad view 
def download_images(request,img_pk):
    try: 
        images = Image.get_image(img_pk)
    except:
        images = None
    if images: 
        for results_image in images:     
            #increment download stats
            Image.increment_download_stat(results_image)
            print(results_image.download_stats)
            response = HttpResponse(results_image.image, content_type='image/jpeg')
            #set title as image's filename, if there is no title, filename will be "Untitled_image"
            if results_image.title:
                filename = results_image.title
            else:
                filename = "Untitled_image"
            response['Content-Disposition'] = 'attachment; filename=%s.jpg' % filename
            return response
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#other photographer's account view 
def othersaccount(request,member_pk):
    member_id_found = Member.find_member(member_pk)
    result_images = Image.retrieve_image_member(member_id_found)
    context={
        'result_images': result_images,'member_id':member_id_found
    }     
    return render(request, 'othersaccount.html', context)

