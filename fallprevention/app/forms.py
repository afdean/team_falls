from django import forms
from django.db import models
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question

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

# class QuestionForm(ModelForm):
#     class Meta:
#         model = Question
#         fields = ['content', 'isKey']

# Hard code 12 questions for now
class QuestionForm(forms.Form):
    CHOICES = (('1', 'Yes',), ('2', 'No',))
    question1 = forms.ChoiceField(
        label = 'I have fallen in the past year',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question2 = forms.ChoiceField(
        label = 'Sometimes I feel unsteady when I am walking',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question3 = forms.ChoiceField(
        label = 'I am worried about falling',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question4 = forms.ChoiceField(
        label = 'I use or have been advised to use a cane or walker to get around safely',
        widget=forms.RadioSelect(attrs={'class':'radio-inline'}), choices=CHOICES,
        required = False,
    )

    question5 = forms.ChoiceField(
        label = 'I steady myself by holding onto furniture when walking at home',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question6 = forms.ChoiceField(
        label = 'I need to push with my hands to stand up from a chair',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question7 = forms.ChoiceField(
        label = 'I have some trouble stepping up onto a curb',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question8 = forms.ChoiceField(
        label = 'I often have to rush to the toilet',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question9 = forms.ChoiceField(
        label = 'I have lost some feeling in my feet',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question10 = forms.ChoiceField(
        label = 'I take medicine that sometimes makes me feel light-headed or more tired than usual',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question11 = forms.ChoiceField(
        label = 'I take medicine to help me sleep or improve my mood',
        widget=forms.RadioSelect, choices=CHOICES,
        required = False,
    )

    question12 = forms.ChoiceField(
        label = 'I often feel sad or depressed',
        widget=forms.RadioSelect, choices=CHOICES,
    )
    #
    # question1 = forms.BooleanField(
    #     label = 'I have fallen in the past year',
    #     required = False,
    # )
    #
    # question2 = forms.BooleanField(
    #     label = 'Sometimes I feel unsteady when I am walking',
    #     required = False,
    # )
    #
    # question3 = forms.BooleanField(
    #     label = 'I am worried about falling',
    #     required = False,
    # )
    #
    # question4 = forms.BooleanField(
    #     label = 'I use or have been advised to use a cane or walker to get around safely',
    #     required = False,
    # )
    #
    # question5 = forms.BooleanField(
    #     label = 'I steady myself by holding onto furniture when walking at home',
    #     required = False,
    # )
    #
    # question6 = forms.BooleanField(
    #     label = 'I need to push with my hands to stand up from a chair',
    #     required = False,
    # )
    #
    # question7 = forms.BooleanField(
    #     label = 'I have some trouble stepping up onto a curb',
    #     required = False,
    # )
    #
    # question8 = forms.BooleanField(
    #     label = 'I often have to rush to the toilet',
    #     required = False,
    # )
    #
    # question9 = forms.BooleanField(
    #     label = 'I have lost some feeling in my feet',
    #     required = False,
    # )
    #
    # question10 = forms.BooleanField(
    #     label = 'I take medicine that sometimes makes me feel light-headed or more tired than usual',
    #     required = False,
    # )
    #
    # question11 = forms.BooleanField(
    #     label = 'I take medicine to help me sleep or improve my mood',
    #     required = False,
    # )
    #
    # question12 = forms.BooleanField(
    #     label = 'I often feel sad or depressed',
    #     required = False,
    # )

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

# Hard code 3 tests for now
class TestForm(forms.Form):

    tg_test = forms.BooleanField(
        label = 'Time up and Go (Recommended)',
        required = False,
    )
    tg_test_details = forms.MultipleChoiceField(
        label = '',
        choices = (
            ('no_problem', "No Problems"),
            ('loss_of_balance', 'Loss of Balance'),
        ),
        initial = None,
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )

    cs_test = forms.BooleanField(
        label = '30 Sec Stand',
        required = False,
    )
    cs_test_details = forms.CharField(
        label = 'Score:',
        required = False,
    )

    balance_test = forms.BooleanField(
        label = '4-stage balance test',
        required = False,
    )
    balance_test_detail1 = forms.CharField(
        label = '1. Stand with your feet side to side:',
        required = False,
    )
    balance_test_detail2 = forms.CharField(
        label = '2. Place the instep of one foot so it is touching the big toe of the other foot:',
        required = False,
    )
    balance_test_detail3 = forms.CharField(
        label = '3. Place the instep of one foot so it is touching the big toe of the other foot:',
        required = False,
    )
    balance_test_detail4 = forms.CharField(
        label = '4. Place the instep of one foot so it is touching the big toe of the other foot:',
        required = False,
    )

    note = forms.CharField(
        label = 'Note:',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
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
    patient_edu = forms.BooleanField(
        label = "Check for Safety Brochure",
        required = False
    )


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
