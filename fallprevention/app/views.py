import urllib as url
import json
from .constants import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
# from app.forms import MessageForm, QuestionForm, LoginForm, LoginCPForm, TugForm, SearchPatientForm, BalanceTestForm, MedicationsForm, ThirtySecStandForm, ResultsForm
from app.forms import *
from app.models import Question, FuncAbilityTest, TestParameter
from app.data_client import DataClient
from app.fhir_reading import FallsFHIRClient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from subprocess import call



# Home screen
def index(request):
    DataClient()
    return render(request, 'app/index.html', {'form': MessageForm()})

def login(request):

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            identity = login_form.cleaned_data['identity']
            print (identity)
            if identity == 'patient':
                # login_form.helper.form_action = '/app/questions/'
                url = '/app/questions/'
                request.session['identity'] = 'patient'
            else:
                # login_form.helper.form_action = '/app/login/care_provider/'
                url = '/app/login/care_provider/'
                request.session['identity'] = 'care_provider'
            return HttpResponseRedirect(url)
    else:
        login_form = LoginForm()

    return render(request, 'app/login.html', {'login_form': login_form})

def login_cp(request):

    if request.method == 'POST':
        login_cp_form = LoginCPForm(request.POST)
        if login_cp_form.is_valid():
            url = '/app/test/'
            request.session['assessments_chosen'] = [];
            return HttpResponseRedirect(url)
    else:
        login_cp_form = LoginCPForm()

    return render(request, 'app/login_cp.html', {'login_cp_form': login_cp_form})

def searchPatient(request):
    if request.method == 'POST':
        search_patient_form = SearchPatientForm(request.POST)
        if search_patient_form.is_valid():
            fhir_client = FallsFHIRClient()
            data_client = DataClient()
            patient_name = search_patient_form.cleaned_data['patient_name'].split()
            # Search for a patient by first and last name
            #TODO error check fot the search result
            data_client.patient = fhir_client.search_patient(patient_name[0], patient_name[1])
            url = '/app/questions/'
            return HttpResponseRedirect(url)
        # if search_patient_form.is_valid():
    else:
        search_patient_form = SearchPatientForm()

    return render(request, 'app/search_patient.html', {'search_patient_form': search_patient_form})

def questions(request):
    data_client = DataClient()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            #second parameter if default value
            if request.session.get('identity', 'patient') == 'patient':
                return HttpResponseRedirect('/app/thankyou/')
            else:
                return HttpResponseRedirect('/app/assessments/')
    else:
        question_form = QuestionForm()
        balance_test_form = BalanceTestForm()

    return render(request, 'app/questions.html', {'question_form': question_form,'balance_test_form':balance_test_form ,  'patient': data_client.patient})

def thankyou(request):
    request.session['assessments_chosen'] = []
    return render(request, 'app/thankyou.html')

# def test(request):

#     # assessments_chosen = request.session.get('assessments_chosen', []);
#     if request.method == 'POST':
#         assessments_form = AssessmentForm(request.POST, assessments_chosen = []);
#         if assessments_form.is_valid():
#             # if assessments_chosen:
#             #     # request.session['assessments_chosen'] = []
#             #     return HttpResponseRedirect('/app/thankyou/')
#             # else:
#             chosen_list = []
#             for field in assessments_form.fields:
#                 if (assessments_form.cleaned_data[field]):
#                     chosen_list.append(field)
#             request.session['assessments_chosen'] = chosen_list
#             # assessments_form = AssessmentForm(assessments_chosen = chosen_list);
#             return HttpResponseRedirect('/app/assessments/details')
#     else:
#         assessments_form = AssessmentForm(assessments_chosen = []);
#     return render(request, 'app/test.html', { 'assessments_form': assessments_form, 'patient': patient})

def assessments_details(request):
    data_client = DataClient()
    assessments_chosen = request.session.get('assessments_chosen', []);
    if request.method == 'POST':
        assessments_form = AssessmentForm(request.POST, assessments_chosen = []);
        if assessments_form.is_valid():
            return HttpResponseRedirect('/app/thankyou')
    else:
        assessments_form = AssessmentForm(assessments_chosen = assessments_chosen);
    return render(request, 'app/assessments.html', { 'assessments_form': assessments_form, 'patient': data_client.patient})

def assessments(request):
     # assessments_chosen = request.session.get('assessments_chosen', []);
    data_client = DataClient()
    if request.method == 'POST':
        assessments_form = AssessmentForm(request.POST, assessments_chosen = []);
        if assessments_form.is_valid():
            # if assessments_chosen:
            #     # request.session['assessments_chosen'] = []
            #     return HttpResponseRedirect('/app/thankyou/')
            # else:
            chosen_list = []
            for field in assessments_form.fields:
                if (assessments_form.cleaned_data[field]):
                    chosen_list.append(field)
            request.session['assessments_chosen'] = chosen_list
            # assessments_form = AssessmentForm(assessments_chosen = chosen_list);
            return HttpResponseRedirect('/app/assessments/details')
    else:
        assessments_form = AssessmentForm(assessments_chosen = []);
    return render(request, 'app/assessments.html', { 'assessments_form': assessments_form, 'patient': data_client.patient})

def medications(request):

    data_client = DataClient()
    if request.method == 'POST':
        medications_form = MedicationsForm(request.POST)
        if medications_form.is_valid():
            return HttpResponseRedirect('/app/thankyou/')
    else:
        medications_form = MedicationsForm()

    return render(request, 'app/medications.html', {'medications_form': medications_form, 'patient': data_client.patient})

def results(request):
    data_client = DataClient()
    results_form = ResultsForm()
    return render(request, 'app/results.html', {'results_form': results_form, 'patient': data_client.patient})

def exams(request):
    data_client = DataClient()
    exams_form = ExamsForm()
    return render(request, 'app/exams.html', {'exams_form': exams_form, 'patient': data_client.patient})

# User Login - Currently not working
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/app/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'app/login.html', {})

def risks(request):
    results_form = ResultsForm()
    return render(request, 'app/risks.html', {'results_form':results_form})
