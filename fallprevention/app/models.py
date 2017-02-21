from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Model for logging key questions in database
@python_2_unicode_compatible
class KeyQuestion(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

# Model for logging additional questions in database
@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

# Model for logging medication list in database
class Medication(models.Model):
    medication_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


@python_2_unicode_compatible
class DummyModel(models.Model):
    dummy_text = models.CharField(max_length=200)

    def __str__(self):
        return self.dummy_text
