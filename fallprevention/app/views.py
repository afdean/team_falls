from django.shortcuts import render
from forms import QuestionForm
from models import Question

# Create your views here.
def index(request):
    return render(request, 'app/index.html',{})

def question_list(request):
    questions = Question.objects.all()
    form = QuestionForm()
    forms = []
    for i in range(0, len(questions)):
        forms.append(QuestionForm(request.POST, instance=questions[i]))
    return render(request, 'app/questions.html', {'form': form, 'questions': questions})