from django import forms

from models import Question

class QuestionForm(forms.ModelForm):
    # answer = forms.BooleanField()

    class Meta:
        model = Question
        fields = ('question_answer',)
