import urllib as url
import json
from .constants import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from app.forms import *
from app.models import Question, FuncAbilityTest, TestParameter
from app.data_client import DataClient
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Home screen
def index(request):
    DataClient()
    return render(request, 'app/index.html', {'form': MessageForm()})

def login(request):
    data_client = DataClient()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            identity = login_form.cleaned_data['identity']
            if identity == 'patient':
                # login_form.helper.form_action = '/app/questions/'
                url = '/app/questions/'
                data_client.identity = 'patient'
                # request.session['identity'] = 'patient'
            else:
                # login_form.helper.form_action = '/app/login/care_provider/'
                url = '/app/login/care_provider/'
                data_client.identity = 'care_provider'
            return HttpResponseRedirect(url)
    else:
        login_form = LoginForm()

    return render(request, 'app/login.html', {'login_form': login_form})

def login_cp(request):
    data_client = DataClient()
    if request.method == 'POST':
        login_cp_form = LoginCPForm(request.POST)
        if login_cp_form.is_valid():
            url = '/app/questions/'
            return HttpResponseRedirect(url)
    else:
        login_cp_form = LoginCPForm()

    return render(request, 'app/login_cp.html', {'login_cp_form': login_cp_form})

def searchPatient(request):
    data_client = DataClient()
    patient_list = []
    if request.method == 'POST':
        search_patient_form = SearchPatientForm(request.POST)
        if search_patient_form.is_valid():
            data_client = DataClient()
            patient_name = search_patient_form.cleaned_data['patient_name'].split()
            # Search for a patient by first and last name
            #TODO error check fot the search result
            patient_list = data_client.fhir_client.search_patient(patient_name[0], patient_name[1])
            if patient_list:
                data_client.patient = patient_list[0]
                data_client.fhir_client.select_patient(data_client.patient['resource']['id'])
                encounter_list = sorted(data_client.fhir_client.search_encounter_all(), key=lambda k: k['resource']['period']['end'], reverse=True)
                if encounter_list:
                    data_client.encounter = encounter_list[0]
                    data_client.fhir_client.select_encounter_from_encounter_result(encounter_list)
                    #print (data_client.fhir_client.encounter_id)
                    # print (data_client.fhir_client.search_observations())
            url = '/app/questions/'
            return HttpResponseRedirect(url)
        # if search_patient_form.is_valid():
    else:
        search_patient_form = SearchPatientForm()

    return render(request, 'app/search_patient.html', {'search_patient_form': search_patient_form, 'patient_list': patient_list})

def questions(request):
    data_client = DataClient()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            score = 0
            key_score = 0
            for i, question in enumerate(data_client.questions['questions']):
                field_name = "question" + str(i)
                answer = question_form.cleaned_data[field_name]
                code = data_client.questions['questions'][i]['code']
                data_client.observations[code] = answer
                flag = False
                # This could be fragile if changed to >=2 falls? Or something non 1
                if isinstance(answer, int):
                    print("If this is an integer, success: " + str(answer))
                    if answer >= 1:
                        flag = True
                else:
                    print("If this is a boolean, success: " + str(answer))
                    flag = answer
                if answer == True:
                    print(question['content'])
                    score += int(data_client.questions['questions'][i]['score'])
                    if data_client.questions['questions'][i]['is_key']:
                        key_score += 1
            if data_client.identity == 'patient':
                return HttpResponseRedirect('/app/thankyou/')
            else:
                # print (data_client.questions['question_logic'])
                if (key_score < data_client.questions['question_logic']['min_key'] and
                    score < data_client.questions['question_logic']['min_score']):
                    data_client.risk_level = "low"
                    return HttpResponseRedirect('/app/risks/')
                return HttpResponseRedirect('/app/assessments/')
    else:
        question_answers = {}
        for i, question in enumerate(data_client.questions['questions']):
            code = data_client.questions['questions'][i]['code']
            if code in data_client.observations:
                field_name = "question" + str(i)
                question_answers[field_name] = data_client.observations[code]
        print(data_client.observations)
        question_form = QuestionForm(initial=question_answers)

    return render(request, 'app/questions.html', {'question_form': question_form, 'patient': data_client.patient})

def thankyou(request):
    data_client = DataClient()
    data_client.assessments_chosen = []
    return render(request, 'app/thankyou.html')

def calculate_age(date_string):
    date_string = date_string.replace('-', '')
    year_string = date_string[0:4]
    month_string = date_string[4:6]
    day_string = date_string[6:8]
    year = int(year_string)
    month = int(month_string)
    day = int(day_string)
    birth_date = date(year, month, day)
    age = date.today() - birth_date
    return math.floor(age.days / 365)

def assessments_details(request):
    data_client = DataClient()
    assessments_chosen = data_client.assessments_chosen
    if request.method == 'POST':
        assessments_form = AssessmentForm(request.POST, assessments_chosen=assessments_chosen);
        if assessments_form.is_valid():
            # Local obs just in case
            observations = {}

            # Boolean to ultimately determine if patient fails GSB
            has_problem = False
            # Score of how many key questions have been answered 'yes' (use 0 because adds 1 each iteration)
            tug_key = 0
            # Minimum amount of key questions needed to be answered 'yes' to fail (use -1 as a check if test conducted)
            tug_min_key = -1
            # Score of how many evaluations have exceeded their respective min time (use 0 because adds 1 each iteration)
            bal_failure = 0
            # Minimum amount of failures for evaluations to fail the test overall (use -1 as a check if test conducted)
            bal_min_failure = -1
            # Minimum amount of time needed for patient to stand in chair (use -1 as a check if test conducted)
            chair_min_failure = -1

            for test in data_client.func_test:
                if test['name'] in data_client.assessments_chosen:
                    if test['code'] == "tug000":
                        tug_min_key = test['min_logic']['min_key']
                    elif test['code'] == "bal000":
                        bal_min_failure = test['min_logic']['min_failure']

                    for i, form in enumerate(test['forms']):
                        field_name = test['code'] + "_form" + str(i)
                        answer = assessments_form.cleaned_data[field_name]
                        code = test['forms'][i]['code']
                        data_client.observations[code] = answer
                        observations[code] = answer

                        # Check logic for TUG
                        if test['code'] == "tug000":
                            # Check for key questions
                            if test['forms'][i]['type'] == 'boolean':
                                if test['forms'][i]['is_key'] and answer:
                                    tug_key = tug_key + 1
                                if test['forms'][i]['code'] == 'tug001' and answer:
                                    # print ("Has problem from cant do it")
                                    has_problem = True
                            # Check for timing scores
                            if test['forms'][i]['type'] == 'integer':
                                # Check to make sure it isnt NoneType
                                if answer is not None:
                                    form_logic = test['forms'][i]['logic']
                                    if form_logic in test['min_logic']:
                                        if answer < test['min_logic'][form_logic]:
                                            # print ("has problem from low time")
                                            has_problem = True

                        # Check logic for 30 Chair
                        if test['code'] == 'chair000':
                            if test['forms'][i]['type'] == 'integer':
                                form_logic = test['forms'][i]['logic']
                                if form_logic in test['min_logic']:
                                    patient_gender = data_client.patient['resource']['gender']
                                    date_string = data_client.patient['resource']['birthDate']
                                    patient_age = calculate_age(date_string)
                                    age_index = test['min_logic']['form_logic']['ages']
                                    male_score = test['min_logic']['form_logic']['male']
                                    female_score = test['min_logic']['form_logic']['female']
                                    if patient_age < ages[0]:
                                        print("Age is less than minimum age for test, will pass since score irrelevant")
                                    if patient_age > ages[-1]:
                                        print("Age is greater than maximum age for test, will fail since score irrelevant")
                                    else:
                                        for i, age in age_index:
                                            if patient_age >= age:
                                                continue
                                            else:
                                                index = i - 1
                                                break
                                    if patient_gender == 'male':
                                        chair_min_failure = male_score[index]
                                    elif patient_gender == 'female':
                                        chair_min_failure = female_score[index]
                                    if answer is not None and chair_min_failure >= 0:
                                        if answer < chair_min_failure:
                                            has_problem = True

                        # Check logic for Balance Test
                        if test['code'] == 'bal000':
                            if test['forms'][i]['type'] == 'integer':
                                form_logic = test['forms'][i]['logic']
                                if form_logic in test['min_logic']:
                                    if answer is not None and answer < test['min_logic'][form_logic]:
                                        bal_score = bal_score + 1

            if tug_min_key >= 0 and tug_key > tug_min_key:
                # print ("has problem from key tugs")
                has_problem = True
            if bal_min_failure >= 0 and bal_score > bal_min_failure:
                # print ('has problem from key bal')
                has_problem = True

            data_client.assessments_chosen = []

            if has_problem:
                if 'q001' in data_client.observations:
                    if data_client.observations['q001']:
                        data_client.risk_level = "high"
                        # print("From FAT, risk level is " + data_client.risk_level)
                        return HttpResponseRedirect('/app/medications/')
                else:
                    data_client.risk_level = "moderate"
                    # print("From FAT, risk level is " + data_client.risk_level)
                    return HttpResponseRedirect('/app/medications/')
            else:
                data_client.risk_level = "low"
                # print("From FAT, risk level is " + data_client.risk_level)
                return HttpResponseRedirect('/app/risks/')

            return HttpResponseRedirect('/app/thankyou')
    else:
        assessments_answers = {}
        for test in data_client.func_test:
            if test['name'] in data_client.assessments_chosen:
                for i, form in enumerate(test['forms']):
                    code = test['forms'][i]['code']
                    if code in data_client.observations:
                        field_name = test['code'] + "_form" + str(i)
                        assessments_answers[field_name] = data_client.observations[code]
        assessments_form = AssessmentForm(initial=assessments_answers, assessments_chosen = assessments_chosen);
    return render(request, 'app/assessments.html', { 'assessments_form': assessments_form, 'patient': data_client.patient})

def assessments(request):
    data_client = DataClient()
    if request.method == 'POST':
        assessments_form = AssessmentForm(request.POST);
        if assessments_form.is_valid():
            chosen_list = []
            for field in assessments_form.fields:
                if (assessments_form.cleaned_data[field]):
                    chosen_list.append(field)
            if not chosen_list:
                return HttpResponseRedirect('/app/assessments/')
            else:
                data_client.assessments_chosen = chosen_list
                return HttpResponseRedirect('/app/assessments/details')
    else:
        assessments_form = AssessmentForm();
    return render(request, 'app/assessments.html', { 'assessments_form': assessments_form, 'patient': data_client.patient})

def medications(request):
    data_client = DataClient()
    if request.method == 'POST':
        medications_form = MedicationsForm(request.POST)
        if medications_form.is_valid():
            if data_client.risk_level == "high":
                return HttpResponseRedirect('/app/exams/')
            elif data_client.risk_level == "moderate":
                return HttpResponseRedirect('/app/risks')
            # Low should only get here through the usage of the side bar
            elif data_client.risk_level == "low":
                return HttpResponseRedirect('/app/risks')
            return HttpResponseRedirect('/app/thankyou/')
    else:
        medications_form = MedicationsForm()

    return render(request, 'app/medications.html', {'medications_form': medications_form, 'patient': data_client.patient})

def exams_details(request):
    data_client = DataClient()
    exams_chosen = data_client.exams_chosen
    if request.method == 'POST':
        exams_form = ExamsForm(request.POST, exams_chosen=exams_chosen)
        if exams_form.is_valid():
            # Local obs just in case
            observations = {}
            for exam in data_client.physical_exam:
                if exam['name'] in exams_chosen:
                    for i, form in enumerate(exam['forms']):
                        field_name = exam['name'] + "_form" + str(i)
                        answer = exams_form.cleaned_data[field_name]
                        code = exam['forms'][i]['code']
                        data_client.observations[code] = answer
                        observations['code'] = answer
            data_client.exams_chosen = []
            # print("The current risk level from exams_details is " + data_client.risk_level)
            return HttpResponseRedirect('/app/risks/')
    else:
        exam_answers = {}
        for exam in data_client.physical_exam:
            if exam['name'] in exams_chosen:
                for i, form in enumerate(exam['forms']):
                    code = exam['forms'][i]['code']
                    if code in data_client.observations:
                        field_name = exam['name'] + "_form" + str(i)
                        exam_answers[field_name] = data_client.observations[code]
        exams_form = ExamsForm(initial=exam_answers, exams_chosen=exams_chosen)
    return render(request, 'app/exams.html', {'exams_form': exams_form, 'patient': data_client.patient})

def exams(request):
    data_client = DataClient()
    if request.method == 'POST':
        exams_form = ExamsForm(request.POST)
        if exams_form.is_valid():
            chosen_list = []
            for field in exams_form.fields:
                if (exams_form.cleaned_data[field]):
                    chosen_list.append(field)
            if not chosen_list:
                return HttpResponseRedirect('/app/exams/')
            else:
                data_client.exams_chosen = chosen_list
                return HttpResponseRedirect('/app/exams/details')
    else:
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
    # put another if that if its empty, do the things that you have ot do pretty pekase

    data_client = DataClient()
    # print ("risk_level:" + data_client.risk_level)
    if data_client.risk_level == "low":
        risks_form = RisksForm(risk_level="low")
    elif data_client.risk_level == "moderate":
        risks_form = RisksForm(risk_level="moderate")
    elif data_client.risk_level == "high":
        # print("In risks, the risk level is high")
        risks_form = RisksForm(risk_level="high")
    else:
        risks_form = RisksForm("incomplete")
    return render(request, 'app/risks.html', {'risks_form':risks_form})
