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

	def __str__(self):
		return self.username

class Image(models.Model):
	title = models.CharField(max_length=30, blank=True)
	tag = models.CharField(max_length=30, blank=True)
	# category = models.CharField(max_length=255, blank=True)
	description = models.TextField(max_length=150, blank=True)
	image = models.ImageField(upload_to='images/',validators=[validate_file_extension])
	uploadtime = models.DateField(auto_now_add=True)
	category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
	owner = models.ForeignKey(Member, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title


