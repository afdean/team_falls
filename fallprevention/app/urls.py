from django.conf.urls import url
from app import views as app_views
from . import views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^questions/$', app_views.questions, name="questions"),
    url(r'^funcabilitytests/$', app_views.test_list, name="test_list"),
    url(r'^login/$', app_views.user_login, name='login'),
    url(r'^searchPatients/$',app_views.searchPatients,name='searchPatients'),
    url(r'^medication/$',app_views.medication, name="medication")
]