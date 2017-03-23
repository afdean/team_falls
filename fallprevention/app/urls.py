from django.conf.urls import url
from app import views as app_views
from . import views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^login/$', app_views.login, name="login"),
    url(r'^login/care_provider/$', app_views.login_cp, name="login_cp"),
    url(r'^search/$', app_views.searchPatient, name="searchPatient"),
    # url(r'^questions/([\w\-]+)/$', app_views.questions, name="questions"),
    url(r'^questions/$', app_views.questions, name="questions"),
    url(r'^thankyou/$', app_views.thankyou, name="thankyou"),
    url(r'^test/$', app_views.test, name="test"),
    url(r'^medications/$', app_views.medications, name="medications"),
    url(r'^results/$', app_views.results, name="results"),
    # url(r'^login/$', views.user_login, name='login'),
]
