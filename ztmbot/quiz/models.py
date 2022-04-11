from django.db import models
from django.utils.translation import gettext as _


class Question(models.Model):

    # Difficulty levels
    LEVEL = (
        (0, _("All")),
        (1, _("Beginner")),
        (2, _("Intermediate")),
        (3, _("Advanced"))
    )

    # Tables for our database
    title = models.CharField(_("Title"), max_length=255)
    points = models.SmallIntegerField(_("Points"))
    difficulty = models.IntegerField(_("Difficulty"), choices=LEVEL, default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


class Answer(models.Model):

    # Adding a foreign key to connect our answers to our questions
    question = models.ForeignKey(Question, related_name="answer", verbose_name=_("Question"), on_delete=models.CASCADE)
    answer = models.CharField(_("Answer"), max_length=255)
    is_correct = models.BooleanField(_("Correct Answer"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.answer
