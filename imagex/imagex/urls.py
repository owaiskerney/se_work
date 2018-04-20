from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
from django.contrib.auth import views as auth_views

app_name = 'mainApp'
urlpatterns = [
    url('^$', views.search, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login_view, name='login'),
    url(r'^logout/',views.logout_view, name='logout'),
    url(r'^signup/',views.signup, name='signup'),     
    url(r'^upload/', views.upload, name='upload'),
    url(r'^search/', views.search, name='search'),
    url(r'^search_photographer/', views.search_photographer, name='search_photographer'),
    url(r'^search_category/', views.search_category, name='search_category'),
     url(r'^browse_by_popularity/', views.browse_by_popularity, name='browse_by_popularity'),
    url(r'^myaccount/',views.myaccount, name='myaccount'),
    url(r'^password_change/',views.password_change, name='password_change'),
  	url(r'^password_reset/$', auth_views.password_reset,
            {'template_name': 'password_reset_form.html'}, 
            name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
            {'template_name': 'password_reset_done.html'}, 
            name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.password_reset_confirm,
            {'template_name': 'password_reset_confirm.html'}, 
            name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
            {'template_name': 'password_reset_complete.html'}, 
            name='password_reset_complete'),
	#url('^',include('django.contrib.auth.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
