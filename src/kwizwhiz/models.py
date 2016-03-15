from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class CommonFields(models.Model):
    """Standard included tracking fields for all tables"""

    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(class)s_set")
    # Typically, you would use signals to set this up, probably combined with a user middleware that gives
    # global access to the request object for the duration of the request.

    class Meta:
        abstract = True


class Lesson(CommonFields):
    """A (non-formal) set of teaching material"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class LessonPrinciple(CommonFields):
    lesson = models.ForeignKey(Lesson)
    content = models.TextField()
    ordering = models.IntegerField(null=True, blank=True)
    questions = models.ManyToManyField('Question', related_name='principles', blank=True)

    class Meta:
        ordering = ['lesson', 'ordering', 'pk']

    def __unicode__(self):
        max_length = 80
        suffix = ""

        if len(self.content) > max_length:
            suffix = "..."

        return "Principle %d - %s%s" % (self.pk, self.content[:max_length], suffix)


class Question(CommonFields):
    ANSWER_CHOICES = (
        (1, 'True',),
        (2, 'False',),
    )

    # An argument can be made either way whether this should have a unique constraint
    content = models.TextField(unique=True)

    answer = models.IntegerField(blank=True, null=True, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True, default='')
    ordering = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['ordering', 'pk']

    def __unicode__(self):
        # TODO: DRY Violation
        max_length = 80
        suffix = ""

        if len(self.content) > max_length:
            suffix = "..."

        return "Question %d - %s%s" % (self.pk, self.content[:max_length], suffix)


# Given the structure above, a quiz class is not actually needed, since quizzes could
# derived from a lesson if they were to only contain one lesson. However, providing
# a Quiz class allows for the tracking of other potential attributes, such as time limits, 
# availability periods, and attempts allowed. It also serves as a more appropriate foreign 
# key for tracking user results.

class Quiz(CommonFields):
    """Defines parameters for quizzing users about lessons."""

    lessons = models.ManyToManyField('Lesson')

    class Meta:
        ordering = ['pk']
        verbose_name_plural = _("Quizzes")

    def __unicode__(self):
        return "Quiz %d on %s" % (self.pk, ', '.join([unicode(x) for x in self.lessons.all()]))


class QuizAttempt(CommonFields):
    """Defines an instance of a user taking a quiz"""

    quiz = models.ForeignKey('Quiz')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="quizattempts")

    class Meta:
        ordering = ['pk']

    def __unicode__(self):
        return "Attempt on %s by %s %s" % (self.quiz, self.user.first_name, self.user.last_name)


class QuizAttemptAnswer(CommonFields):
    """Defines one answer submitted by a user to a question"""

    # Going to break 5NF here, perhaps...
    quiz_attempt = models.ForeignKey('QuizAttempt')
    question = models.ForeignKey('Question')

    # Argue over whether to name this value or answer
    answer = models.IntegerField(blank=True, null=True, choices=Question.ANSWER_CHOICES)

    class Meta:
        ordering = ('quiz_attempt', 'question__ordering', 'question')
        unique_together = ('quiz_attempt', 'question',)

    def __unicode__(self):
        return "QuizAttemptAnswer %d" % self.pk
