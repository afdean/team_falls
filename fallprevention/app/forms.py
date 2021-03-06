from django import forms
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question
from app.data_client import DataClient

def validate_search_patient(patient_name):
    # validate patient name (must have first name and last name)
    patient_name_list = patient_name.split()
    if (len(patient_name_list) != 2 and len(patient_name_list) != 3):
        raise ValidationError(
            "Please input the full name of the patient"
        )

def generate_form(field, field_widget=None, field_choices=None, is_required=False):
    if field['type'] == "boolean":
        return forms.BooleanField(
            label=field['content'],
            required=is_required,
        )
    elif field['type'] == "choice_bool":
        return forms.TypedChoiceField(
            label=field['content'],
            widget=field_widget,
            choices=field_choices,
            required=is_required,
            # Can't coerce bool, because cleaned_data returns unicode string, which is
            # always true if the string isn't empty, i.e "". Lambda is a work around
            coerce=lambda x: x=="True"
        )
    elif field['type'] == "choice_int":
        return forms.TypedChoiceField(
            label=field['content'],
            widget=field_widget,
            choices=field_choices,
            required=is_required,
            # Can't coerce bool, because cleaned_data returns unicode string, which is
            # always true if the string isn't empty, i.e "". Lambda is a work around
            coerce=int
        )
    elif field['type'] == "integer":
        return forms.IntegerField(
            label=field['content'],
            min_value=0,
            widget=forms.NumberInput,
            required=field['is_required'],
            help_text=field['help_text']
        )
    elif field['type'] == "char":
        return forms.CharField(
            label=field['content'],
            required=is_required,
            # widget=forms.Textarea,
            help_text=field['help_text']
        )

class LoginForm(forms.Form):
    identity = forms.TypedChoiceField(
        label='Identify who you are',
        choices=(('patient', 'Patient'),
                ('care_provider', 'Care Provider')),
        required=True,
    )
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForms'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

class LoginCPForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        max_length=80,
        required=True,
    )
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput,
        max_length=80,
        required=True,
    )
    def __init__(self, *args, **kwargs):
        super(LoginCPForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginCPForms'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

class LoginPatientForm(forms.Form):
    username = forms.CharField(
        label="Username:",
        max_length=80,
        required=True,
    )
    password = forms.CharField(
        label="Password:",
        widget=forms.PasswordInput,
        max_length=80,
        required=True,
    )
    def __init__(self, *args, **kwargs):
        super(LoginCPForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginCPForms'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

class SearchPatientForm(forms.Form):
    patient_name = forms.CharField(
        label="Patient Name:",
        max_length=80,
        required=True,
        validators=[validate_search_patient]
    )

    def __init__(self, *args, **kwargs):
        super(SearchPatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-searchPatientForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Search'))

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for i, question in enumerate(data_client.questions['questions']):
            code = data_client.questions['questions'][i]['code']
            field_name = code
            choice_list = []
            for choice_pair in question['choices']:
                pair_array = []
                pair_array.append(choice_pair["value"])
                pair_array.append(choice_pair["text"])
                choice_list.append(pair_array)
            choice_tuple = tuple(tuple(x) for x in choice_list)
            self.fields[field_name] = generate_form(question, forms.RadioSelect, field_choices=choice_tuple)
            # Could expand on standards doc by requiring things to be filled in dynamically
            self.fields[field_name].required = True
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))

    def clean(self):
        """
        This is a custom override
        """
        data_client = DataClient()
        cleaned_data = super(QuestionForm, self).clean()
        num_falls = cleaned_data.get("q001")
        injury = cleaned_data.get("q003")

        if injury and num_falls == 0:
            msg = "It is not possible to have been injured without having a fall"
            self.add_error('q001', msg)
            self.add_error('q003', msg)
            raise forms.ValidationError("Please fix the fields")

        # Could set obs. here to have in record despite incomplete?
        return cleaned_data

class AssessmentDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assessments_chosen = kwargs.pop("assessments_chosen", None)
        super(AssessmentDetailsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        # assessments_chosen = data_client.assessments_chosen
        self.helper = FormHelper()
        self.helper.layout = Layout()
        i = 0
        if assessments_chosen:
            # self.helper.layout.append(HTML (
            #     <span id="hiddenTag" style="display: none">{{ i }}</span>
            # ))
            # self.helper.layout.append(Button (
            # ))
            for test in data_client.func_test:
                if test['code'] in assessments_chosen:

                    code = test['code']
                    test_fieldset = Fieldset(test['name'], css_class=test['name'])
                    # self.helper.layout.append(Button(test['code'], test['code']))
                    for i, form in enumerate(test['forms']):
                        code = test['forms'][i]['code']
                        field_name = code
                        self.fields[field_name] = generate_form(form, None, None)
                        test_fieldset.append(Field(field_name))
                        # self.fields[field_name].widget = forms.HiddenInput()
                    self.helper.layout.append(test_fieldset)
            self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_id = 'id-assessmentForm'
        self.helper.form_method = 'post'

    def clean(self):
        """
        This is a custom override
        """
        data_client = DataClient()
        problem_list = []
        cleaned_data = super(AssessmentDetailsForm, self).clean()
        cant_tug = cleaned_data.get("tug001")
        tug_time = cleaned_data.get("tug002")
        no_problems = cleaned_data.get("tug003")
        error = False
        for test in data_client.func_test:
            if test['code'] == "tug000":
                for field in test['forms']:
                    if field['is_problem']:
                        problem_list.append(field['code'])

        if cant_tug is not None and cant_tug:
            if tug_time is not None:
                time_msg = "Either uncheck the box above or please leave this blank"
                self.add_error('tug002', time_msg)
                error = True
            if no_problems is not None and no_problems:
                prob_msg = "It is not possible to unable to do the TUG while having timed score or no problems"
                self.add_error('tug001', prob_msg)
                error = True

        if no_problems is not None and no_problems:
            msg = "It is not possible to have no problems checked off with other problems"
            for code in problem_list:
                if code in cleaned_data and cleaned_data[code]:
                    self.add_error(code, msg)
                    error = True

        if error:
            raise forms.ValidationError("Please fix the fields")

        # Could set obs. here to have in record despite incomplete?
        return cleaned_data

class AssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AssessmentForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        # assessments_chosen = data_client.assessments_chosen
        self.helper = FormHelper()
        self.helper.layout = Layout()
        field_set = Fieldset("Please select assessment(s) to complete")
        for test in data_client.func_test:
            if test['code'] in data_client.observations:
                self.fields[test['code']] = forms.BooleanField(
                    label=test['name'] + " (Completed)",
                    required=False,
                )
            elif test['is_recommended']:
                self.fields[test['code']] = forms.BooleanField(
                    label=test['name'] + " (Recommended)",
                    required=False,
                )
            else:
                self.fields[test['code']] = forms.BooleanField(
                    label=test['name'],
                    required=False,
                )
            field_set.append(Field(test['code']))
        self.helper.layout.append(field_set)
        self.helper.add_input(Submit('submit', 'Next'))
        self.helper.form_id = 'id-assessmentForm'
        self.helper.form_method = 'post'

    def clean(self):
        """
        This is a custom override
        """
        data_client = DataClient()
        cleaned_data = super(AssessmentForm, self).clean()
        selected_tests = False
        for exam, value in cleaned_data.items():
            if value:
                selected_tests = True
                break
        if not selected_tests:
            raise forms.ValidationError("Please select at least one exam")
        return cleaned_data
        # Could set obs. here to have in record despite incomplete?
        return cleaned_data

class NoteForm(forms.Form):
    note = forms.CharField(
        widget=forms.Textarea,
        label='Note:',
        required=False,
    )

class MedicationsForm(forms.Form):
    #hard code medications for now, will generate it dynamically next step
    def __init__(self, *args, **kwargs):
        super(MedicationsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
        # self.helper.layout = Layout()
        for i, form in enumerate(data_client.med_form['forms']):
            code = data_client.med_form['forms'][i]['code']
            field_name = code
            self.fields[field_name] = generate_form(form)
        # self.helper.layout.append(checked_medications)
        self.helper.add_input(Submit('submit', 'Submit'))

class ProblemsForm(forms.Form):
    problems = forms.CharField(
        label = 'Problems',
        required = False,
    )
    def __init__(self, *args, **kwargs):
        super(ProblemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class MedicationsLinkedForm(forms.Form):
    medicationsLinked = forms.CharField(
        label = 'Medications linked to Falls',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(MedicationsLinkedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-medicationLinkedForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

def is_int(str):
    try:
        int(str)
        return True
    except:
        return False

class ExamsDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        exams_chosen = kwargs.pop("exams_chosen", None)
        super(ExamsDetailsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        self.helper.layout = Layout()
        if exams_chosen:
            for exam in data_client.physical_exam:
                if exam['code'] in exams_chosen:
                    exam_fieldset = Fieldset(exam['name'], css_class=exam['name'])
                    for i, form in enumerate(exam['forms']):
                        code = exam['forms'][i]['code']
                        field_name = code
                        self.fields[field_name] = generate_form(form)
                        exam_fieldset.append(Field(field_name))
                    self.helper.layout.append(exam_fieldset)
            self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_id = 'id-examsForm'
        self.helper.form_method = 'post'

    def clean(self):
        """
        This is a custom override
        """

        data_client = DataClient()
        problem_list = []
        cleaned_data = super(ExamsDetailsForm, self).clean()

        left = cleaned_data.get("vis001")
        right = cleaned_data.get("vis002")
        both = cleaned_data.get("vis003")
        eye_list = []
        if left != None:
            eye_list.append(("vis001", left))
        if right != None:
            eye_list.append(("vis002", right))
        if both != None:
            eye_list.append(("vis003", both))

        supine = cleaned_data.get("pos001")
        standing = cleaned_data.get("pos002")
        standing3 = cleaned_data.get("pos003")
        pressure_list = []
        if supine != None:
            pressure_list.append(("pos001", supine))
        if standing != None:
            pressure_list.append(("pos002", standing))
        if standing3 != None:
            pressure_list.append(("pos003", standing3))

        # This needs to be cleaned up: standards should have fields indicating the type of entry they should have.
        # For example, this one would be vision, another could just be "" if you can enter whatever you want
        print("Here is the eye list")
        print (eye_list)

        for s in eye_list:
            if s[1] is not None and len(s[1]) > 0 and '/' in s[1]:
                print(s)
                index = s[1].find('/', 0, len(s[1]))
                if index != -1:
                    first_str = s[1][0:index]
                    second_str = s[1][index + 1:len(s[1])]
                    if is_int(first_str) and is_int(second_str):
                        first_num = int(first_str)
                        second_num = int(second_str)
                        if first_num != 20:
                            self.add_error(s[0], "Must be in form \"20/20\": Please ensure the first number is equal to 20")
                        if second_num <= 0:
                            self.add_error(s[0], "Must be in form \"20/20\": Please ensure the second number is positive")
                    else:
                        self.add_error(s[0], "Must be in form \"20/20\": Please ensure numbers are correctly formatted")
                else:
                    self.add_error(s[0], "Must be in form \"20/20\": Please ensure \"/\" is in entry")
            else:
                self.add_error(s[0], "Must be in form \"20/20\"")

        for s in pressure_list:
            if s[1] is not None and len(s[1]) > 0 and '/' in s[1]:
                print(s)
                index = s[1].find('/', 0, len(s[1]))
                if index != -1:
                    first_str = s[1][0:index]
                    second_str = s[1][index + 1:len(s[1])]
                    if is_int(first_str) and is_int(second_str):
                        first_num = int(first_str)
                        second_num = int(second_str)
                        if first_num <= 20:
                            self.add_error(s[0], "Must be in form \"120/80\": Please ensure the first number is positive")
                        if second_num <= 0:
                            self.add_error(s[0], "Must be in form \"120/80\": Please ensure the second number is positive")
                    else:
                        self.add_error(s[0], "Must be in form \"120/80\": Please ensure numbers are correctly formatted")
                else:
                    self.add_error(s[0], "Must be in form \"120/80\": Please ensure \"/\" is in entry")
            else:
                self.add_error(s[0], "Must be in form \"120/80\"")



        return cleaned_data

class ExamsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExamsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        completed = []
        obs = data_client.observations
        for exam in data_client.physical_exam:
            for form in exam['forms']:
                if form['code'] in obs:
                    completed.append(exam['code'])
                    break
        self.helper = FormHelper()
        self.helper.layout = Layout()
        field_set = Fieldset("Please select exam(s) to complete")
        for exam in data_client.physical_exam:
            if exam['code'] in completed:
                self.fields[exam['code']] = forms.BooleanField(
                label=exam['name'] + " (Completed)",
                required=False,
            )
            else:
                self.fields[exam['code']] = forms.BooleanField(
                label=exam['name'],
                required=False,
            )

            field_set.append(Field(exam['code']))
        self.helper.layout.append(field_set)
        self.helper.add_input(Submit('submit', 'Next'))
        self.helper.form_id = 'id-examsForm'
        self.helper.form_method = 'post'

    def clean(self):
        """
        This is a custom override
        """
        data_client = DataClient()
        cleaned_data = super(ExamsForm, self).clean()
        selected_exams = False
        for exam, value in cleaned_data.items():
            if value:
                selected_exams = True
                break
        if not selected_exams:
            raise forms.ValidationError("Please select at least one exam")
        return cleaned_data

class RisksForm(forms.Form):
    """
    This is a generic results form that will show every intervention
    """
    def __init__(self, *args, **kwargs):
        risk_level = kwargs.pop("risk_level", None)
        incomplete = kwargs.pop("incomplete_list", None)
        super(RisksForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        self.helper.layout = Layout()

        intervention_list = []
        print(risk_level)
        if risk_level == "low" or risk_level == "incomplete":
            for intervention in data_client.risk_list["risks"]["low_risk"]:
                intervention_list.append(intervention)
        elif risk_level == "moderate":
            for intervention in data_client.risk_list["risks"]["moderate_risk"]:
                intervention_list.append(intervention)
        elif risk_level == "high":
            for intervention in data_client.risk_list["risks"]["high_risk"]:
                intervention_list.append(intervention)
        print(intervention_list)
        # Pythonic way to check if list isn't empty
        if intervention_list:
            for intervention in intervention_list:
                current_intervention = data_client.intervention_list[intervention]
                intervention_fieldset = Fieldset(current_intervention['name'], css_class='field_set_results')
                for i, form in enumerate(current_intervention['forms']):
                    code = current_intervention['forms'][i]['code']
                    field_name = code
                    self.fields[field_name] = generate_form(form)
                    intervention_fieldset.append(Field(field_name))
                self.helper.layout.append(intervention_fieldset)
            print("here")

        self.helper.form_id = 'id-risksForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Complete'))
