from django.conf.urls import url
from app import views as app_views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^questions/$', app_views.questions, name="questions"),
    url(r'^funcabilitytests/$', app_views.test_list, name="test_list"),
    url(r'^login/$', app_views.user_login, name='login'),
]

