from django.contrib import admin

# Register your models here.
from .models import Question, Medication, FuncAbilityTest, TestParameter

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'score', 'is_key', 'reason')

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FuncAbilityTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_recommended', 'video_link', 'pdf_link',)

class TestParameterAdmin(admin.ModelAdmin):
    list_display = ('test_key', 'content', 'risk',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(FuncAbilityTest, FuncAbilityTestAdmin)
admin.site.register(TestParameter, TestParameterAdmin)
