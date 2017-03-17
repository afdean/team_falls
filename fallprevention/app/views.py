from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MessageForm, QuestionForm, LoginForm, LoginCPForm, TestForm, SearchPatientForm
from .models import Question, FuncAbilityTest, TestParameter
# from subprocess import call
import urllib.request, json


# Create your views here.
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

def searchPatient(request, searchItem):

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
    return render(request, 'app/test.html', {'test_form': test_form, 'patient': patient})

def test_list(request):
    tests = FuncAbilityTest.objects.all()
    return render(request, 'app/funcabilitytests.html', {'tests': tests})
