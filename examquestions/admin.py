from django.contrib import admin
from .models import Question, ExamName, ExamTemplate, Result, AttemptedQuestion,Start_exam_user
from users.models import UsersConfig
from django import forms

class UsersConfigAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone', 'state', 'city', 'gender', 'otp_verification')
    search_fields = ('email', 'username', 'phone', 'state', 'city')
    list_filter = ('state', 'city', 'gender', 'otp_verification')

admin.site.register(UsersConfig, UsersConfigAdmin)

class QuestionAdminForm(forms.ModelForm):
    CORRECT_ANSWER_CHOICES = (
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    )

    correct_answer = forms.ChoiceField(choices=CORRECT_ANSWER_CHOICES)

    class Meta:
        model = Question
        fields = '__all__'

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'option1', 'option2', 'option3', 'option4', 'correct_answer', 'difficulty_level')
    #list_editable = ('correct_answer',)
    # formfield_overrides = {
    #     models.CharField: {'widget': Select(choices=(('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')))}
    # }

admin.site.register(Question, QuestionAdmin)

class ExamNameAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration')

admin.site.register(ExamName, ExamNameAdmin)

class ExamTemplateAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(ExamTemplate, ExamTemplateAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'timestamp')

admin.site.register(Result, ResultAdmin)

class AttemptedQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'chosen_option', 'is_correct', 'exam')

admin.site.register(AttemptedQuestion, AttemptedQuestionAdmin)

admin.site.register(Start_exam_user)