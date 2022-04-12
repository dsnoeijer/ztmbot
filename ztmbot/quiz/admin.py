from django.contrib import admin
from . import models


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'answer',
        'is_correct'
    ]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'cat',
        'points',
        'difficulty'
    ]

    list_dislay = [
        'title',
        'updated_at'
    ]

    # Add answer fields to our Add Question page
    inlines = [
        AnswerInlineModel
    ]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer',
        'is_correct',
        'question'
    ]
