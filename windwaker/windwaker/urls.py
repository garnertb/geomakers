from django.conf.urls import patterns, include, url
from django.contrib import admin
from skyshaker import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^skyshaker/', include('skyshaker.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^donate/', views.donate, name='donate'),
    url(r'projects/(?P<slug>[^\.]+)', views.project, name='project'),
    url(r'^profiles/(?P<slug>[^\.]+)', views.profile, name='profile'),
    url(r'^search/', views.search, name='search'),
    url(r'^contribute/$', views.contribute, name='contribute'),
#    url(r'^geodream/$', views.geodream, name='geodream'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
