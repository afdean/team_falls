
# Fall Prevention Project
Repo for Georgia Tech CS6440 group Team Falls

## Overview
This is a Clinical Decision Support FHIR app for to assist physicians in fall prevention support for the elderly.

### Andy's Notes (change later)
If there are any issues running commands, consider deleting the migration files, and running the flush command to reinitalize

1. Initialize the database (if not already initialized)
   
    * python manage.py makemigrations
    * python manage.py migrate
    * python manage.py loaddata initial.json

2. Run query checks
    * python manage.py shell
    * from app.models import Question, FuncAbilityTest, TestParameter
    * Below are a list of possible queries to check if it initialized properly, in order
    * q = Question.objects.all()
    * f = FuncAbilityTest.objects.all()
    * g = f[0]
    * p = g.testparameter_set.all()
    * t = p[0]
    * k = t.test_key

