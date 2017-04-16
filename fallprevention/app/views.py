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
    # Wipe whatever is in memory...?
    # data_client = DataClient().clean()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            identity = login_form.cleaned_data['identity']
            if identity == 'patient':
                url = '/app/login/patient/'
                data_client.identity = 'patient'
            elif identity == "care_provider":
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
            url = '/app/search/'
            return HttpResponseRedirect(url)
    else:
        login_cp_form = LoginCPForm()
    return render(request, 'app/login_cp.html', {'login_cp_form': login_cp_form})

def login_patient(request):
    data_client = DataClient()
    if request.method == 'POST':
        login_cp_form = LoginCPForm(request.POST)
        if login_cp_form.is_valid():
            print("I am here")
            url = '/app/questions/'
            return HttpResponseRedirect(url)
    else:
        login_cp_form = LoginCPForm()
        print("I am here 2")
    return render(request, 'app/login_cp.html', {'login_cp_form': login_cp_form})

def search_patient(request):
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
        if data_client.identity != "care_provider":
            return HttpResponseRedirect('/app/login/')

    return render(request, 'app/search_patient.html', {'search_patient_form': search_patient_form, 'patient_list': patient_list})

def questions(request):
    data_client = DataClient()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            # try:
            #     question_form.check_injury()
            # except forms.ValidationError as e:
            #     return HttpResponseRedirect('/app/questions/')
            # if question_form.check_injury():
            #     return HttpResponseRedirect('/app/questions/')
            print("I got to this point!")
            score = 0
            key_score = 0
            for i, question in enumerate(data_client.questions['questions']):
                code = data_client.questions['questions'][i]['code']
                field_name = code
                answer = question_form.cleaned_data[field_name]
                data_client.observations[code] = answer
                flag = False
                # This could be fragile if changed to >=2 falls? Or something non 1
                if isinstance(answer, int):
                    if answer >= 1:
                        flag = True
                else:
                    flag = answer
                if flag:
                    score += int(data_client.questions['questions'][i]['score'])
                    if data_client.questions['questions'][i]['is_key']:
                        key_score += 1
            questions_code = data_client.questions['code']
            if (key_score < data_client.questions['question_logic']['min_key'] and
                score < data_client.questions['question_logic']['min_score']):
                data_client.observations[questions_code] = "Pass"
            else:
                data_client.observations[questions_code] = "Fail"
            print(data_client.observations)
            if data_client.identity == 'patient':
                return HttpResponseRedirect('/app/thankyou/')
            else:
                calculate_risk()
                if data_client.risk_level == "incomplete":
                    return HttpResponseRedirect('/app/assessments/')
                elif data_client.risk_level is not None:
                    return HttpResponseRedirect('/app/risks/')
    else:
        question_answers = {}
        for i, question in enumerate(data_client.questions['questions']):
            code = data_client.questions['questions'][i]['code']
            if code in data_client.observations:
                code = data_client.questions['questions'][i]['code']
                field_name = code
                question_answers[field_name] = data_client.observations[code]
        print(data_client.observations)
        question_form = QuestionForm(initial=question_answers)

    if data_client.identity == "patient":
        return render(request, 'app/questions_patient.html', {'question_form': question_form, 'patient': data_client.patient})
    else:
        return render(request, 'app/questions.html', {'question_form': question_form, 'patient': data_client.patient})

def thankyou(request):
    data_client = DataClient()
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
    """
    If there's anything in this project that needs refactoring, this is it.
    """
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
            bal_score = 0
            tug_conducted = False
            bal_conducted = False
            chair_conducted = False

            for test in data_client.func_test:
                if test['code'] in data_client.assessments_chosen:
                    # Pulls required fields to evaluate logic
                    if test['code'] == "tug000":
                        tug_min_key = test['min_logic']['min_key']
                        tug_conducted = True
                    elif test['code'] == "bal000":
                        bal_min_failure = test['min_logic']['min_failure']
                        bal_conducted = True
                    elif test['code'] == "chair000":
                        chair_conducted = True

                    for i, form in enumerate(test['forms']):
                        code = test['forms'][i]['code']
                        field_name = code
                        answer = assessments_form.cleaned_data[field_name]
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
                                    data_client.observations["tug000"] = "Fail"
                            # Check for timing scores
                            if test['forms'][i]['type'] == 'integer':
                                # Check to make sure it isnt NoneType
                                if answer is not None:
                                    form_logic = test['forms'][i]['logic']
                                    if form_logic in test['min_logic']:
                                        if answer < test['min_logic'][form_logic]:
                                            # print ("has problem from low time")
                                            has_problem = True
                                            data_client.observations["tug000"] = "Fail"

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
                                            data_client.observations["chair000"] = "Fail"

                        # Check logic for Balance Test
                        if test['code'] == 'bal000':
                            if test['forms'][i]['type'] == 'integer':
                                # Bug here: what if logic doesn't exist?
                                form_logic = test['forms'][i]['logic']
                                if form_logic in test['min_logic']:
                                    # However, still force them to enter 0 so that the field is acknowledged
                                    if answer is None:
                                        bal_score = bal_score + 1
                                    if answer is not None and answer < test['min_logic'][form_logic]:
                                        bal_score = bal_score + 1

            # Final logic checks for tests
            if tug_min_key >= 0 and tug_key > tug_min_key:
                # print ("has problem from key tugs")
                has_problem = True
                data_client.observations["tug000"] = "Fail"
            if bal_min_failure >= 0 and bal_score > bal_min_failure:
                # print ('has problem from key bal')
                has_problem = True
                data_client.observations["bal000"] = "Fail"
            if tug_conducted:
                if "tug000" not in data_client.observations:
                    data_client.observations["tug000"] = "Pass"
            if bal_conducted:
                if "bal000" not in data_client.observations:
                    data_client.observations["bal000"] = "Pass"
            if chair_conducted:
                if "chair000" not in data_client.observations:
                    data_client.observations["chair000"] = "Pass"


            # Wipe clean for next iteration through, if desired to do more assessments
            data_client.assessments_chosen = []

            # Call calculate_risk at this point...
            calculate_risk()

            if has_problem:
                if data_client.risk_level == "incomplete":
                    return HttpResponseRedirect('/app/risks/')
                else:
                    return HttpResponseRedirect('/app/medications/')
            else:
                return HttpResponseRedirect('/app/risks/')

    else:
        assessments_answers = {}
        for test in data_client.func_test:
            if test['code'] in data_client.assessments_chosen:
                for i, form in enumerate(test['forms']):
                    code = test['forms'][i]['code']
                    if code in data_client.observations:
                        field_name = code
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
    calculate_risk()
    if request.method == 'POST':
        medications_form = MedicationsForm(request.POST)
        if medications_form.is_valid():
            if data_client.risk_level == "high":
                return HttpResponseRedirect('/app/exams/')
            else:
                return HttpResponseRedirect('/app/risks/')
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
                if exam['code'] in exams_chosen:
                    for i, form in enumerate(exam['forms']):
                        code = exam['forms'][i]['code']
                        field_name = code
                        answer = exams_form.cleaned_data[field_name]
                        data_client.observations[code] = answer
                        observations[code] = answer
            # Clear this for the next iteration...
            data_client.exams_chosen = []
            # Exams is last stop before risks, all levels go to risks including incomplete
            return HttpResponseRedirect('/app/risks/')
    else:
        exam_answers = {}
        for exam in data_client.physical_exam:
            if exam['code'] in exams_chosen:
                for i, form in enumerate(exam['forms']):
                    code = exam['forms'][i]['code']
                    if code in data_client.observations:
                        field_name = code
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
    data_client = DataClient()
    incomplete_list = calculate_risk()
    risk_level = data_client.risk_level
    print("Here is the list of incomplete tasks: ")
    print(incomplete_list)
    print("The risk level is currently: " + data_client.risk_level)
    if data_client.risk_level == "low":
        risks_form = RisksForm(risk_level="low")
    elif data_client.risk_level == "moderate":
        risks_form = RisksForm(risk_level="moderate")
    elif data_client.risk_level == "high":
        risks_form = RisksForm(risk_level="high")
    else:
        risks_form = RisksForm(risk_level="incomplete", incomplete_list=incomplete_list)
    return render(request, 'app/risks.html', {'risks_form':risks_form, 'risk_level': risk_level, 'incomplete_list': incomplete_list})

def calculate_risk():
    """
    Function that updates the current status of the risk level based on what's written in the observation list
    That is, it can be called at any time to know the status of the risk level
    Returns a list of things yet to be completed
    """
    data_client = DataClient()
    obs = data_client.observations

    # Set to "Pass" and "Fail"
    question_fail = None
    assessment_fail = None

    num_falls = None
    injury = None
    incomplete_list = []
    question_code = data_client.questions['code']
    tests = data_client.func_test
    test_codes = []
    for test in tests:
        test_codes.append(test['code'])

    # Check if questions have been completed
    if question_code in obs:
        question_fail = obs["q000"]
        num_falls = obs["q001"]
        injury = obs["q003"]

    # Check each test; If one has failed then assesment_fail is fail guaranteed
    for code in test_codes:
        if code in obs and obs[code] == "Fail":
            assessment_fail = "Fail"
            break

    # If wasn't set to True above but one of the tests is in obs, then the patient had no problems, and so they passed
    for code in test_codes:
        if code in obs:
            if assessment_fail == None:
                assessment_fail = "Pass"

    # Algorithm
    if question_fail is None:
        data_client.risk_level = "incomplete"
        incomplete_list.append("Fall Screening")

    if assessment_fail is None:
        incomplete_list.append("Assessments")

    if question_fail is not None:
        if assessment_fail is None:
            if question_fail == "Pass":
                data_client.risk_level = "low"
            else:
                data_client.risk_level = "incomplete"
        elif assessment_fail == "Fail":
            if num_falls > 1:
                data_client.risk_level = "high"
            elif num_falls == 1:
                # Unnecessary check but just in case
                if injury:
                    data_client.risk_level = "high"
                elif not injury:
                        data_client.risk_level = "moderate"
            elif num_falls == 0:
                data_client.risk_level = "moderate"
        # Note that by just doing a FAT, and passing it, then you are low risk anyway
        # The decision is made to return "incomplete" even if there's a pass for assessment and nothing
        # for questions, since they are rather crucial to know about, and screening is fast.
        elif assessment_fail == "Pass":
            data_client.risk_level = "low"

    return incomplete_list



