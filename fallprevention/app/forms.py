from django import forms
from django.db import models
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question
from .data_client import DataClient

class LoginForm(forms.Form):
    identity = forms.TypedChoiceField(
        label = 'Identify Who you are',
        choices = (('patient', 'Patient'),
                ('care_provider', 'Care Provider')),
        required = True,
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
        label = "Username:",
        max_length = 80,
        required = True,
    )
    password = forms.CharField(
        label = "Password:",
        widget = forms.PasswordInput,
        max_length = 80,
        required = True,
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
        label = "Patient Name:",
        max_length = 80,
        required = True,
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
        CHOICES = (('1', 'Yes',), ('2', 'No',))
        for i, question in enumerate(data_client.questions.questions):
            fieldName = "question" + str(i)
            self.fields[fieldName] = forms.ChoiceField(
                label = question.content,
                widget=forms.RadioSelect, choices = CHOICES,
                required = False,
            )
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

# Hard code 3 tests for now
class TestForm(forms.Form):

    note = forms.CharField(
        label = 'Note:',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for i, test in enumerate(data_client.func_test):
            fieldName = test.name
            self.fields[fieldName] = forms.BooleanField(
                label = test.name,
                required = False,
            )
        self.helper = FormHelper()
        self.helper.form_id = 'id-testForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class MedicationsForm(forms.Form):

    #hard code medications for now, will generate it dynamically next step
    medications = forms.MultipleChoiceField(
        choices = (
            ('asprin', "Asprin"),
            ('isosorbide', 'Isosorbide'),
            ('amitriptyline', 'Amitriptyline')
        ),
        initial = None,
        required = False,
        widget = forms.CheckboxSelectMultiple,
        help_text = "<strong>Note:</strong> This is helper text placeholder.",
    )

    problems = forms.CharField(
        label = 'Problems',
        required = False,
    )

    medicationsLinked = forms.CharField(
        label = 'Medications linked to Falls',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(MedicationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-medicationForms'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

class ResultsForm(forms.Form):
    #Hard code an example results page. Until we figure out how to do it dynamically.
    safety_brochure = forms.BooleanField(
        label = "Check for Safety Brochure",
        required = False
    )

    prevent_falls = forms.BooleanField(
        label = "What Can You Do to Prevent Falls",
        required = False
    )

    vitamin_d = forms.BooleanField(
        label = "Patient is currently taking at least 800 IU of Vitamin D",
        required = False
    )

    calcium = forms.BooleanField(
        label = "Patient is currently taking enough calcium",
        required = False
    )

    gsb_pt = forms.BooleanField(
        label = "PT to improve gait, strength and balance",
        required = False
    )

    exercise_program = forms.BooleanField(
        label = "Fall prevention/Community exercise program",
        required = False
    )

    review_safety = forms.BooleanField(
        label = "Reviewed home safety with patient",
        required = False
    )

    def __init__(self, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Patient Education (Handouts)',
                'safety_brochure'
            ),
            Fieldset(
                'Vitamin D and Calcium',
                'vitamin_d',
                'calcium'
            ),
            Fieldset(
                'Referrals',
                'gsb_pt',
                'exercise_program'
            ),
            Fieldset(
                'Home Safety',
                'review_safety'
            )

        )
        self.helper.form_id = 'id-resultsForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))



class MessageForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
