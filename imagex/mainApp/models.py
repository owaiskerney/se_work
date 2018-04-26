from django.db import models
from .validators import validate_file_extension
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.auth import authenticate


#Tag model for tags associated with images
class Tag(models.Model):
	name=models.CharField(max_length=20)
	def __str__(self):
		return self.name

	def search_tag(keyword):
		return Tag.objects.get(name=str(keyword))

	

#Category model for image categories
class Category(models.Model):
	name = models.CharField(max_length=30,\
		choices=(['Abstract','Abstract'],['Aerial','Aerial'],['Animals','Animals'],['Architecture','Architecture'],\
		['Black and White','Black and White'],['Family','Family'],['Fashion','Fashion'],['Fine Art','Fine Art'],\
		['Food','Food'],['Journalism','Journalism'],['Landscape','Landscape'],['Macro','Macro'],['Nature','Nature'],\
		['Night','Night'],['People','People'],['Performing Arts','Performing Arts'],['Sport','Sport'],['Still Life','Still Life'],\
		['Street','Street'],['Travel','Travel']))
	#Returns category object according to category name
	def find_cat_id(category_name):
		return Category.objects.get(name=str(category_name))


	class Meta: 
		ordering = ['name']
		
#Member model representing registered users	
class Member(AbstractUser):
	
	avatar = models.ImageField(upload_to='avatars/',validators=[validate_file_extension], blank=True)
	self_description = models.TextField(max_length=30,blank=True)


	class Meta(AbstractUser.Meta):
		pass
	#Returns member object according to member name
	def find_member(keyword):
		return Member.objects.get(username=str(keyword))
	#Checks if login information is correct for an existing member
	def check_member(username,password):
		user = authenticate(username=username,password=password)
		return user
	#Returns member profile
	def get_profile(member_id):
		return Member.objects.filter(id=member_id)

	
#Image model for images in the system
class Image(models.Model):
	title = models.CharField(max_length=30, blank=True)	
	description = models.TextField(max_length=150, blank=True)
	image = models.ImageField(upload_to='images/',validators=[validate_file_extension])
	uploadtime = models.DateField(auto_now_add=True)
	tag = models.ManyToManyField(Tag, blank=True) #Tags of the image, related to tag model
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) #Category of the image, related to category model
	owner = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True) #temporary use for demo
	like_stats=models.IntegerField(default=0)
	download_stats=models.IntegerField(default=0)
	popularity=models.IntegerField(default=0)
	likeby = models.ManyToManyField(Member, related_name ='likeby', blank=True)
	
	#Returns images belonging to a certain category
	def retrieve_image_category(cat_id_found):
		return_images= Image.objects.filter(category=cat_id_found)
		return return_images

	#Returns images belonging to a certain member
	def retrieve_image_member(member_id):
		return_images= Image.objects.filter(owner=member_id)
		return return_images

	#Returns image-tag combination
	def image_has_tag(image_id, tag_id):
		return Image.objects.filter(id=image_id, tag=tag_id)
	
	#Checks if total number of images uploaded by a member is under the limit
	def check_number_limit(member_id):
		return Image.objects.filter(owner=member_id).count()

	#Checks if total images uploaded by member in a day is under the limit
	def check_frequency_limit(member_id,date):
		return Image.objects.filter(owner=member_id, uploadtime=date).count()

	#Returns category object according to category name
	def get_image(image_id):
		return Image.objects.filter(id=image_id)

	#Checking if image is already liked by a member
	def check_already_liked(image_id, user_id):
		return Image.objects.filter(id=image_id,likeby=user_id)
	
	#Increasing download statistics for an image
	def increment_download_stat(Image):
		Image.download_stats = Image.download_stats+1
		Image.save()


	
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
        
		self.popularity = self.like_stats + self.download_stats
		return super(Image, self).save(*args, **kwargs)



#Token model for token used to sign up
class Token(models.Model):
	email = models.EmailField(null = True, blank = True, max_length = 30)
	tokenCode = models.IntegerField()

	
	def check_token(token,email):
		tokens = Token.objects.filter(tokenCode=token,email=email)            
		token_available = False
		if tokens:
			token_availabe = True
		return token_available

	def generate_token(email):
		tokenCode = random.randint(100000,999999)
		Token.objects.create(email = email, tokenCode = tokenCode).save()
		return tokenCode

#Gallery model for image galleries in the system
class Gallery(models.Model):
	name=models.CharField(max_length=20)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) #Category of the gallery, related to category model
	image = models.ManyToManyField(Image) #Images in the gallery, related to Image model
	tag = models.ManyToManyField(Tag) #Tags of the image, related to tag model
	user=models.ManyToManyField(Member)

	def __str__(self):
		return self.title




