from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from .core import views

urlpatterns = patterns('',
    url(r'^skyshaker/', include('geomakers.core.urls')),
    url(r'^community-guidelines/$', views.community, name='community'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^donate/', views.donate, name='donate'),
    url(r'projects/(?P<slug>[^\./]+)$', views.project, name='project'),
    url(r'projects/(?P<slug>[^\./]+)/edit$', views.projectEdit, name='projectEdit'),
    url(r'^profiles/(?P<slug>[^\./]+)$', views.profile, name='profile'),
    url(r'^profiles/(?P<slug>[^\./]+)/edit$', views.profileEdit, name='profileEdit'),
    url(r'^search/', views.search, name='search'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^makerspaces/$', views.makerspaces, name='makerspaces'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^team/$', views.team, name='team'),
    url(r'^donate/$', views.donate, name='donate'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
#    url(r'^geodream/$', views.geodream, name='geodream'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^geoboosts/$', views.geoboosts, name='geoboosts'),
    url(r'^geodreams/$', views.geodreams, name='geodreams'),
    url(r'^georecipes/$', views.georecipes, name='georecipes'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
