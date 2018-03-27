from django.contrib import admin


# Register your models here.
from .models import User
from .models import Member
from .models import Image
from .models import Gallery
from .models import Category
from .models import Tag

#admin.site.register(User)
admin.site.register(Member)
admin.site.register(Image)
admin.site.register(Gallery)
admin.site.register(Category)
admin.site.register(Tag)
