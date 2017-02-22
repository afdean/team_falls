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

# Dummy model to experiment with
@python_2_unicode_compatible
class DummyModel(models.Model):
    dummy_text = models.CharField(max_length=200)

    def __str__(self):
        return self.dummy_text
