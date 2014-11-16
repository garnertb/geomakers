import views
from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^community-guidelines/$', views.community, name='community'),
    url(r'projects/(?P<slug>[^\./]+)$', views.project, name='project'),
    url(r'projects/(?P<slug>[^\./]+)/edit$', views.projectEdit, name='projectEdit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profiles/(?P<slug>[^\./]+)$', views.profile, name='profile'),
    url(r'^profiles/(?P<slug>[^\./]+)/edit$', views.profileEdit, name='profileEdit'),
    url(r'^search/', views.search, name='search'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^makerspaces/$', views.makerspaces, name='makerspaces'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^team/$', views.team, name='team'),
    url(r'^donate/$', views.donate, name='donate'),
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
