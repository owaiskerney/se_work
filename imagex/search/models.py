from django.db import models
from .validators import validate_file_extension

class Category(models.Model):
	name = models.CharField(max_length=30,\
		choices=(['Abstract','Abstract'],['Aerial','Aerial'],['Animals','Animals'],['Architecture','Architecture'],\
		['Black and White','Black and White'],['Family','Family'],['Fashion','Fashion'],['Fine Art','Fine Art'],\
		['Food','Food'],['Journalism','Journalism'],['Landscape','Landscape'],['Macro','Macro'],['Nature','Nature'],\
		['Night','Night'],['People','People'],['Performing Arts','Performing Arts'],['Sport','Sport'],['Still Life','Still Life'],\
		['Street','Street'],['Travel','Travel']))

	def __str__(self):
		return self.name

	class Meta: 
		ordering = ['name']

class Member(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=15)
	avatar = models.ImageField(upload_to='avatars/',validators=[validate_file_extension])
	email = models. EmailField(max_length=30)
	self_description = models.TextField(max_length=30,blank=True)

	#Add user as foreign id?
	user=models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.username

class Image(models.Model):
	title = models.CharField(max_length=30, blank=True)
	#tag = models.CharField(max_length=30, blank=True)

	
	description = models.TextField(max_length=150, blank=True)
	image = models.ImageField(upload_to='images/',validators=[validate_file_extension])
	uploadtime = models.DateField(auto_now_add=True)
	tag = models.ManytoManyField(Tag) #Tags of the image, related to tag model
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) #Category of the image, related to category model
	owner = models.ForeignKey(Member, on_delete=models.CASCADE) #
	like_stats=models.IntegerField(default=0)
	download_stats=models.IntegerField(default=0)
	
	def __str__(self):
		return self.title


class Tag(models.Model):
	name=models.CharField(max_length=20)


class User(models.Model):
	#What to add? What about many to many with images and other associations


class Gallery(models.Model):
	name=models.CharField(max_length=20)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE) #Category of the gallery, related to category model
	image = models.ManytoManyField(image) #Images in the gallery, related to Image model
	tag = models.ManytoManyField(Tag) #Tags of the image, related to tag model



