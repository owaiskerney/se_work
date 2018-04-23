from django.contrib import admin


# Register your models here.
from .models import *


#admin.site.unregister(User)
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Image)
admin.site.register(Gallery)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Token)