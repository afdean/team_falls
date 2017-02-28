from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Model for logging questions in database
@python_2_unicode_compatible
class Question(models.Model):
    # The question itself
    content = models.CharField(max_length=200)

    # Value of score provided if answered 'yes', pulled from brochure
    score = models.IntegerField(default=1)

    # Indicates if it's a key question or not
    isKey = models.BooleanField(default=False)

    # Reason why the question is relevant
    reason = models.CharField(max_length=200)

    def __str__(self):
        return self.content

# Model for logging medication list linked to falls in database
@python_2_unicode_compatible
class Medication(models.Model):
    # Name for the medication
    name = models.CharField(max_length=200)

    # Will need more fields as a pharmacist/specialist shows us more

    def __str__(self):
        return self.name

# Model for checking test information
@python_2_unicode_compatible
class FuncAbilityTest(models.Model):
    # Name of the test
    name = models.CharField(max_length=200)

    # Whether or not the test is recommended
    isRecommended = models.BooleanField(default=False)

    # Link to youtube video of the test
    videoLink = models.URLField(max_length=500)

    # Link to PDF on how to conduct the test
    pdfLink = models.URLField(max_length=500)

    def __str__(self):
        return self.name

# Model for mapping parameters to FuncAbilityTest
@python_2_unicode_compatible
class TestParameter(models.Model):
    # Name of the parameter
    testKey = models.ForeignKey(FuncAbilityTest, on_delete=models.PROTECT)

    # Parameter information
    content = models.CharField(max_length=200)

    # Boolean for parameter if it indicates increased risk (and if relevant)
    risk = models.BooleanField(default=False)

    def __str__(self):
        return self.content
