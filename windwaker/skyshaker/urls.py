from django.conf.urls import patterns, url
from skyshaker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'projects/(?P<slug>[^\.]+)', views.project, name='project'),
)
