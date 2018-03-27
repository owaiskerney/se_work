from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

urlpatterns = [
    url('^$', views.index, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login, name='login'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^search/', views.search, name='search')

    #url('', include('mainApp.urls'))
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
