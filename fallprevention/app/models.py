from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Model for logging questions in database
@python_2_unicode_compatible
class Question(models.Model):
    # The question itself
    question_text = models.CharField(max_length=200)

    # Value of score provided if answered 'yes', pulled from brochure
    question_score = models.IntegerField(default=1)

    # Indicates if it's a key question or not
    question_key = models.BooleanField(default=False)

    # Reason why the question is relevant
    question_why = models.CharField(max_length=200)

    # Answer supplied
    question_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

# Model for logging medication list linked to falls in database
@python_2_unicode_compatible
class Medication(models.Model):
    # Name for the medication
    medication_name = models.CharField(max_length=200)

    # Will need more fields as a pharmacist/specialist shows us more

    def __str__(self):
        return self.medication_name

# Model for checking test information
@python_2_unicode_compatible
class FuncAbilityTest(models.Model):
    # Name of the test
    test_name = models.CharField(max_length=200)

    # Whether or not the test is recommended
    test_rec = models.BooleanField(default=False)

    # Link to youtube video of the test
    test_link = models.URLField(max_length=500)

    # Link to PDF on how to conduct the test
    test_instruct = models.URLField(max_length=500)

    def __str__(self):
        return self.test_name

# Model for mapping parameters to FuncAbilityTest
@python_2_unicode_compatible
class TestParameter(models.Model):
    # Name of the parameter
    parameter_testkey = models.ForeignKey(FuncAbilityTest, on_delete=models.PROTECT)

    # Parameter information
    parameter_text = models.CharField(max_length=200)

    # Boolean for parameter if it indicates increased risk (and if relevant)
    parameter_risk = models.BooleanField(default=False)

    def __str__(self):
        return self.parameter_text

# Dummy model to experiment with
@python_2_unicode_compatible
class DummyModel(models.Model):
    dummy_text = models.CharField(max_length=200)

    def __str__(self):
        return self.dummy_text
