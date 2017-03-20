from django.shortcuts import render
# from urllib import request, json
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MessageForm, QuestionForm, LoginForm, LoginCPForm, TestForm, SearchPatientForm, MedicationsForm
from .models import Question, FuncAbilityTest, TestParameter
# from subprocess import call
from six.moves import urllib
import json


# Home screen
def index(request):
    # url = "./fixtures/initial.json"
    # response = urllib.request.urlopen(url)
    # with open('initial.json') as data_file:
    #     data = json.load(data_file)
    data_file = open("./app/fixtures/initial.json", "r")
    data = json.load(data_file)

    print (data)
    # This view is missing all form handling logic for simplicity of the example
    # call(["python", "manage.py", "makemigrations"])
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
            url = '/app/search/patient/'
            # login_cp_form.helper.form_action = url
            return HttpResponseRedirect(url)
    else:
        login_cp_form = LoginCPForm()

    return render(request, 'app/login_cp.html', {'login_cp_form': login_cp_form})

def searchPatient(request):

    if request.method == 'POST':
        search_patient_form = SearchPatientForm(request.POST)
        if search_patient_form.is_valid():
            patient = { 'name' : search_patient_form.cleaned_data['patient_name'] }
            request.session['patient'] = patient
            url = '/app/questions/'
            return HttpResponseRedirect(url)
        # if search_patient_form.is_valid():
    else:
        search_patient_form = SearchPatientForm()

    return render(request, 'app/search_patient.html', {'search_patient_form': search_patient_form})

def questions(request):
    # questions = Question.objects.all()

    # forms = []
    # for i in range(0, len(questions)):
    #     forms.append(QuestionForm(request.POST, instance=questions[i]))
    # return render(request, 'app/questions.html', {'form': form, 'questions': questions})

    patient = request.session.get('patient', '')
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            #second parameter if default value
            if request.session.get('identity', 'patient') == 'patient':
                return HttpResponseRedirect('/app/thankyou/')
            else:
                return HttpResponseRedirect('/app/test/')
    else:
        question_form = QuestionForm()

    return render(request, 'app/questions.html', {'question_form': question_form, 'patient': patient})

def thankyou(request):
    return render(request, 'app/thankyou.html')

def test(request):
    patient = request.session.get('patient', '')
    test_form = TestForm()
    # test_form.fields['test2'].widget = forms.HiddenInput()
    return render(request, 'app/test.html', {'test_form': test_form, 'patient': patient})

def medications(request):

    patient = request.session.get('patient', '')
    if request.method == 'POST':
        medications_form = MedicationsForm(request.POST)
        if medications_form.is_valid():
            return HttpResponseRedirect('/app/thankyou/')
    else:
        medications_form = MedicationsForm()

    return render(request, 'app/medications.html', {'medications_form': medications_form, 'patient': patient})

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