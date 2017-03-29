from django import forms
from django.db import models
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from .models import Question
from app.data_client import DataClient

def generate_form(field, field_widget=None, field_choices=None, isHidden=None):
    if field.type == "boolean":
        return forms.BooleanField(
            label=field.content,
            required=False,
        )
    elif field.type == "choice":
        return forms.ChoiceField(
            label=field.content,
            widget=field_widget,
            choices=field_choices,
            required=False,
        )
    elif field.type == "integer":
        return forms.IntegerField(
            label=field.content,
            required=False,
        )
    elif field.type == "char":
        return forms.CharField(
            label=field.content,
            required=False,
        )
    if isHidden:
        self.fields[field_name].widget = forms.HiddenInput()

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
            field_name = "question" + str(i)
            self.fields[field_name] = generate_form(question, forms.RadioSelect, CHOICES)
        self.helper = FormHelper()
        self.helper.form_id = 'id-questionsForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

# class TugForm(forms.Form):
#     tg_test_details = forms.MultipleChoiceField(
#         label = '',
#         choices = (
#             ('no_problem', "No Problems"),
#             ('loss_of_balance', 'Loss of Balance'),
#             ('steady_self_on_walls', 'Steadying Self on Walls'),
#             ('shuffling', 'Shuffling'),
#             ('short_stride', 'Short Stride'),
#             ('little_or_no_arm_swing', 'Little or no arm swing'),
#             ('en_bloc_turning', 'En bloc turning'),
#             ('not_using_assitive_device_properly', 'Not using assitive device properly'),
#         ),
#         initial = None,
#         required = False,
#         widget = forms.CheckboxSelectMultiple,
#     )

class TugForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TugForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test.name == "Timed Up and Go Test":
                tug_test = test
                break
        for i, form in enumerate(tug_test.forms):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

# class ThirtySecStandForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(ThirtySecStandForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-balance'
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Submit'))
#
#     cs_test_details = forms.CharField(
#         label = 'Score:',
#         required = False,
#     )

class ThirtySecStandForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ThirtySecStandForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test.name == "30-Second Chair Stand":
                thirty_test = test
                break
        for i, form in enumerate(thirty_test.forms):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

# class BalanceTestForm(forms.Form):
#     balance_test_detail1 = forms.CharField(
#         label = '1. Stand with your feet side to side:',
#         required = False,
#     )
#     balance_test_detail2 = forms.CharField(
#         label = '2. Place the instep of one foot so it is touching the big toe of the other foot:',
#         required = False,
#     )
#     balance_test_detail3 = forms.CharField(
#         label = '3. Place the instep of one foot so it is touching the big toe of the other foot:',
#         required = False,
#     )
#     balance_test_detail4 = forms.CharField(
#         label = '4. Place the instep of one foot so it is touching the big toe of the other foot:',
#         required = False,
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(BalanceTestForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-balance'
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Submit'))

class BalanceTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BalanceTestForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        for test in data_client.func_test:
            if test.name == "4 Stage Balance Test":
                balance_test = test
                break
        for i, form in enumerate(balance_test.forms):
            field_name = "form" + str(i)
            self.fields[field_name] = generate_form(form)
        self.helper = FormHelper()
        self.helper.form_id = 'id-tugform2'
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
        super(ExamsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        j = 0
        self.helper.layout = Layout()
        for exam in data_client.physical_exam:
            exam_fieldset = Fieldset(exam.name)
            for i, form in enumerate(exam.forms):
                field_name = str(j)
                j = j + 1
                self.fields[field_name] = generate_form(form)
                exam_fieldset.append(Field(field_name))
            self.helper.layout.append(exam_fieldset)
        self.helper.form_id = 'id-tugform2'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class ResultsForm(forms.Form):
    """
    This is a generic results form that will show every intervention
    """
    def __init__(self, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        data_client = DataClient()
        self.helper = FormHelper()
        j = 0
        self.helper.layout = Layout()
        for intervention in data_client.intervention_list:
            intervention_fieldset = Fieldset(intervention.name)
            for i, form in enumerate(intervention.forms):
                field_name = str(j)
                j = j + 1
                self.fields[field_name] = generate_form(form)
                intervention_fieldset.append(Field(field_name))
            self.helper.layout.append(intervention_fieldset)
        self.helper.form_id = 'id-tugform2'
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
