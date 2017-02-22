from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^questions/$', views.question_list, name="question_list"),
    url(r'^funcabilitytests/$', views.test_list, name="test_list")
]
