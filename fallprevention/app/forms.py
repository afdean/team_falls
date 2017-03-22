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
        required = False,
    )

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

# Hard code 3 tests for now
class TugForm(forms.Form):

    tg_test_details = forms.MultipleChoiceField(
        label = '',
        choices = (
            ('no_problem', "No Problems"),
            ('loss_of_balance', 'Loss of Balance'),
            ('steady_self_on_walls', 'Steadying Self on Walls'),
            ('shuffling', 'Shuffling'),
            ('short_stride', 'Short Stride'),
            ('little_or_no_arm_swing', 'Little or no arm swing'),
            ('en_bloc_turning', 'En bloc turning'),
            ('not_using_assitive_device_properly', 'Not using assitive device properly'),
        ),
        initial = None,
        required = False,
        widget = forms.CheckboxSelectMultiple,
    )
class ThirtySecStandForm(forms.Form):
     cs_test_details = forms.CharField(
        label = 'Score:',
        required = False,
    )

def __init__(self, *args, **kwargs):
        super(ThirtySecStandForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-balance'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class BalanceTestForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(BalanceTestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-balance'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class NoteForm(forms.Form):
    note = forms.CharField(
        widget=forms.Textarea,
        label = 'Note:',
        required = False,
    )



class MedicationsForm(forms.Form):
    #hard code medications for now, will generate it dynamically next step
     asprin = forms.CharField(
        label = 'Asprin',
        required = False,
    )
isosorbide = forms.CharField(
        label = 'Isosorbide',
        required = False,
    )
def __init__(self, *args, **kwargs):
        super(MedicationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-problemsForms'
        self.helper.form_method = 'post'
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