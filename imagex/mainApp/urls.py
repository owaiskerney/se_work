from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
 #url(r'^upload$', views.upload, name='upload'),
 #url(r'^search$', views.search, name='search' )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)