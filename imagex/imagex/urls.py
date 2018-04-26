from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
from mainApp.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views

app_name = 'mainApp'
urlpatterns = [
    url(r'^$', views.browse_by_popularity_homepage, name='homepage'),
    url(r'^homepage/', views.browse_by_popularity_homepage, name='homepage'),
    url(r'^browse_by_popularity_homepage/', views.browse_by_popularity_homepage, name='browse_by_popularity_homepage'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login_view, name='login'),
    url(r'^logout/',views.logout_view, name='logout'),
    url(r'^signup/',views.signup, name='signup'),     
    url(r'^upload/', views.upload, name='upload'),
    url(r'^delete/(?P<img_pk>.*)$', views.delete, name='delete'),
    url(r'^search/', views.search, name='search'),
    url(r'^myaccount/',views.myaccount, name='myaccount'),
    url(r'^password_change/',views.password_change, name='password_change'),
  	url(r'^password_reset/$', auth_views.password_reset,
            {'template_name': 'password_reset_form.html','html_email_template_name': 'password_reset_email.html',
        'subject_template_name': 'password_reset_subject.txt','password_reset_form': EmailValidationOnForgotPassword},
            name='password_reset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done,
            {'template_name': 'password_reset_done.html'}, 
            name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth_views.password_reset_confirm,
            {'template_name': 'password_reset_confirm.html'}, 
            name='password_reset_confirm'),
    url(r'^reset_done/$', auth_views.password_reset_complete,
            {'template_name': 'password_reset_complete.html'}, 
            name='password_reset_complete'),
    url(r'^invite/', views.invite, name='invite'),
    url(r'^invite_done/', views.invite_done, name='invite_done'),
    url(r'^edit_profile/',views.edit_profile, name='edit_profile'),
    url(r'^like_images/',views.like_images, name='like_images'),
    url(r'^download_images/(?P<img_pk>.*)$',views.download_images, name='download_images'),
    url(r'^othersaccount/(?P<member_pk>.*)$', views.othersaccount, name='othersaccount'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
