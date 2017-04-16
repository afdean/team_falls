from django import forms
from django.db import models
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question
from app.data_client import DataClient

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
            required=is_required,
            help_text=field['help_text']
        )
    elif field['type'] == "char":
        return forms.CharField(
            label=field['content'],
            required=is_required,
            widget=forms.Textarea,
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
            print("This was reached")
            msg = "It is not possible to have been injured without having a fall"
            self.add_error('q001', msg)
            self.add_error('q003', msg)
            raise forms.ValidationError("Please fix the fields")

        # Could set obs. here to have in record despite incomplete?
        return cleaned_data

class AssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assessments_chosen = kwargs.pop("assessments_chosen", None)
        super(AssessmentForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        # assessments_chosen = data_client.assessments_chosen
        self.helper = FormHelper()
        self.helper.layout = Layout()
        if assessments_chosen:
            for test in data_client.func_test:
                if test['code'] in assessments_chosen:
                    test_fieldset = Fieldset(test['name'], css_class=test['name'])
                    for i, form in enumerate(test['forms']):
                        code = test['forms'][i]['code']
                        field_name = code
                        self.fields[field_name] = generate_form(form, None, None)
                        test_fieldset.append(Field(field_name))
                        # self.fields[field_name].widget = forms.HiddenInput()
                    self.helper.layout.append(test_fieldset)
            self.helper.add_input(Submit('submit', 'Submit'))
        else:
            for test in data_client.func_test:
                if test['is_recommended']:
                    self.fields[test['code']] = forms.BooleanField(
                        label=test['name'] + " (Recommended)",
                        required=False,
                    )
                else:
                    self.fields[test['code']] = forms.BooleanField(
                        label=test['name'],
                        required=False,
                    )
            self.helper.add_input(Submit('submit', 'Next'))
        self.helper.form_id = 'id-assessmentForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Next'))


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
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    asprin = forms.CharField(
        label = 'Asprin',
        required = False,
    )
    isosorbide = forms.CharField(
        label = 'Isosorbide',
        required = False,
    )

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

class ExamsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        exams_chosen = kwargs.pop("exams_chosen", None)
        super(ExamsForm, self).__init__(*args, **kwargs)
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
        else:
            for exam in data_client.physical_exam:
                self.fields[exam['code']] = forms.BooleanField(
                    label=exam['name'],
                    required=False,
                )
            self.helper.add_input(Submit('submit', 'Next'))
        self.helper.form_id = 'id-examsForm'
        self.helper.form_method = 'post'
<<<<<<< HEAD
        self.helper.add_input(Submit('submit', 'Next'))
=======
>>>>>>> origin/master

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

        if risk_level == "low":
            for intervention in data_client.risk_list["risks"]["low_risk"]:
                intervention_list.append(intervention)
        elif risk_level == "moderate":
            for intervention in data_client.risk_list["risks"]["moderate_risk"]:
                intervention_list.append(intervention)
        elif risk_level == "high":
            for intervention in data_client.risk_list["risks"]["high_risk"]:
                intervention_list.append(intervention)

        # Pythonic way to check if list isn't empty
        if intervention_list:
            for intervention in intervention_list:
                current_intervention = data_client.intervention_list[intervention]
                intervention_fieldset = Fieldset(current_intervention['name'], css_class='field_set_results')
                for i, form in enumerate(current_intervention['forms']):
                    field_name = current_intervention['name'] + "_form" + str(i)
                    self.fields[field_name] = generate_form(form)
                    intervention_fieldset.append(Field(field_name))
                self.helper.layout.append(intervention_fieldset)

        self.helper.form_id = 'id-risksForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
