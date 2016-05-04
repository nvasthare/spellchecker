from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<l>[0-4])/(?P<words>[0-1])/$', views.post_edit, name='post_edit'),

]
