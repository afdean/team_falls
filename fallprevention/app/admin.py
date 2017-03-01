from django.contrib import admin

# Register your models here.
from .models import Question, Medication, FuncAbilityTest, TestParameter

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'score', 'isKey', 'reason')

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FuncAbilityTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'isRecommended', 'videoLink', 'pdfLink',)

class TestParameterAdmin(admin.ModelAdmin):
    list_display = ('testKey', 'content', 'risk',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(FuncAbilityTest, FuncAbilityTestAdmin)
admin.site.register(TestParameter, TestParameterAdmin)
