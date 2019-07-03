from django.conf.urls import url
from .views import *

app_name = 'post'

urlpatterns = [
    url(r'^Index/$', post_index, name='index'),
    url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
    url(r'^Create/$', post_create, name='create'),
    url(r'^Update/$', post_update, name='update'),
    url(r'^Delete/$', post_delete, name='delete'),

]
