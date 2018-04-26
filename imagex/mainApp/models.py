from django.db import models
from .validators import validate_file_extension
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


#class User(models.Model):
#	def __str__(self):
#		return self.title
#Search_image function implementation
	#def search_image(keyword):


class Tag(models.Model):
	name=models.CharField(max_length=20)
	def __str__(self):
		return self.name

	def search_tag(keyword):
		return Tag.objects.get(name=str(keyword))

	#search_tag function implementation
	#Remember to fix url for this
	#def search_tag(keyword):


class Category(models.Model):
	name = models.CharField(max_length=30,\
		choices=(['Abstract','Abstract'],['Aerial','Aerial'],['Animals','Animals'],['Architecture','Architecture'],\
		['Black and White','Black and White'],['Family','Family'],['Fashion','Fashion'],['Fine Art','Fine Art'],\
		['Food','Food'],['Journalism','Journalism'],['Landscape','Landscape'],['Macro','Macro'],['Nature','Nature'],\
		['Night','Night'],['People','People'],['Performing Arts','Performing Arts'],['Sport','Sport'],['Still Life','Still Life'],\
		['Street','Street'],['Travel','Travel']))

	def find_cat_id(category_name):
		return Category.objects.get(name=str(category_name))

 


	#def __str__(self):
	#	return self

	class Meta: 
		ordering = ['name']
		
class Member(AbstractUser):
	#username = models.CharField(max_length=20)
	#password = models.CharField(max_length=15)
	avatar = models.ImageField(upload_to='avatars/',validators=[validate_file_extension], blank=True)
	#email = models. EmailField(max_length=30)
	self_description = models.TextField(max_length=30,blank=True)

	#Add user as foreign id
	# user=models.OneToOneField(User, on_delete=models.CASCADE)
	# REQUIRED_FIELDS = ('user',)

	class Meta(AbstractUser.Meta):
		pass

	def find_member(keyword):
		return Member.objects.get(username=str(keyword))

	# def __str__(self):
	#  	return self.user.username

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
	# user=models.ManyToManyField(User)
	def retrieve_image_category(cat_id_found):
		return_images= Image.objects.filter(category=cat_id_found)
		return return_images

	def retrieve_image_member(member_id):
		return_images= Image.objects.filter(owner=member_id)
		return return_images

	def image_has_tag(image_id, tag_id):
		return Image.objects.filter(id=image_id, tag=tag_id)
	
	def check_upload_limit(member_id):
		return Image.objects.filter(owner=member_id).count()

	def check_frequency_limit(member_id,date):
		return Image.objects.filter(owner=member_id, uploadtime=date).count()

	def get_image(image_id):
		return Image.objects.filter(id=image_id)

	def check_already_liked(image_id, user_id):
		return Image.objects.filter(id=image_id,likeby=user_id)


	
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
        
		self.popularity = self.like_stats + self.download_stats
		return super(Image, self).save(*args, **kwargs)



#implementing retrieve_image function
	#def retrieve_image(image_id):

class Token(models.Model):
	email = models.EmailField(null = True, blank = True, max_length = 30)
	tokenCode = models.IntegerField()

class Gallery(models.Model):
	name=models.CharField(max_length=20)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) #Category of the gallery, related to category model
	image = models.ManyToManyField(Image) #Images in the gallery, related to Image model
	tag = models.ManyToManyField(Tag) #Tags of the image, related to tag model
	user=models.ManyToManyField(Member)

	def __str__(self):
		return self.title




