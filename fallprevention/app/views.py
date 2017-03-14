from django.shortcuts import render

from .forms import QuestionForm
from .models import Question, FuncAbilityTest, TestParameter
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


# Home screen
def index(request):
    return render(request, 'app/index.html',{})
  
def questions(request):
    # questions = Question.objects.all()
    # form = QuestionForm()
    # forms = []
    # for i in range(0, len(questions)):
    #     forms.append(QuestionForm(request.POST, instance=questions[i]))
    # return render(request, 'app/questions.html', {'form': form, 'questions': questions})

    questions = Question.objects.all()
    if request.method == 'POST':

        form = QuestionForm(request.POST)
        if form.is_valid():
            answers = form.cleaned_data['answers']
            return HttpResponse(answers)

    else:
        form = QuestionForm()

    return render(request, 'app/questions.html', {'form': form, 'questions': questions})

def test_list(request):
    tests = FuncAbilityTest.objects.all()
    print(tests)
    return render(request, 'app/funcabilitytests.html', {'tests': tests})
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
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'app/login.html', {})

# View used to search patients
def searchPatients(request):
    return render(request,'app/searchPatients.html',{})

#View used to view patient history
# A patient dict is needed to populated with info
def history(request):
    return render(request,'app/history.html',{})

#View used for medication screen
def medication(request):
    return render(request,'app/medication.html',{})

