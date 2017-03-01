from django.conf.urls import url
from app import views as app_views
from . import views

urlpatterns = [
    url(r'^app/$', app_views.index, name="index"),
    url(r'^questions/$', app_views.questions, name="questions"),
    url(r'^funcabilitytests/$', app_views.test_list, name="test_list"),
    url(r'^login/$', views.user_login, name='login'),
]

