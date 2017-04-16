from django.conf.urls import url
from app import views as app_views
from . import views

urlpatterns = [
    url(r'^$', app_views.index, name="index"),
    url(r'^login/$', app_views.login, name="login"),
    url(r'^login/care_provider/$', app_views.login_cp, name="login_cp"),
    url(r'^login/patient/$', app_views.login_patient, name="login_patient"),
    url(r'^search/$', app_views.search_patient, name="search_patient"),
    url(r'^questions/$', app_views.questions, name="questions"),
    url(r'^thankyou/$', app_views.thankyou, name="thankyou"),
    url(r'^assessments/$', app_views.assessments, name="assessments"),
    url(r'^assessments/details$', app_views.assessments_details, name="assessments_details"),
    url(r'^medications/$', app_views.medications, name="medications"),
    url(r'^exams/$', app_views.exams, name="exams"),
    url(r'^exams/details$', app_views.exams_details, name="exams_details"),
    url(r'^risks/$', app_views.risks, name="risks"),
]
