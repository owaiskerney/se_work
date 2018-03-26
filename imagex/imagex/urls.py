from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from upload import views

urlpatterns = [
    url('^$', views.home, name='home'),
    path('upload/', include('upload.urls')),
    path('search/', include('search.urls')),
    url(r'^admin/', admin.site.urls),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
