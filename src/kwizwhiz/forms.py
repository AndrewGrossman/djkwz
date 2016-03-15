from django import forms
from .models import Lesson, Quiz, QuizAttemptAnswer, Question
from django.utils.translation import ugettext_lazy as _
from django.forms import modelformset_factory


class LessonSelectForm(forms.Form):
    lesson = forms.ModelChoiceField(Lesson.objects.all(), empty_label=_("Select a Lesson") + "...",
                                  widget=forms.Select(attrs={'onchange': "this.form.submit();"}))


class QuizSelectForm(forms.Form):
    quiz = forms.ModelChoiceField(Quiz.objects.all(), empty_label=_("Select a Quiz") + "...",
                                  widget=forms.Select(attrs={'onchange': "this.form.submit();"}))



# Pressed for time, using the below found solution
# http://stackoverflow.com/questions/5824037/how-to-get-rid-of-the-bogus-choice-generated-by-radioselect-of-django-form
# BEGIN----
from itertools import chain
from django.forms import RadioSelect
from django.utils.encoding import force_unicode

class RadioSelectNotNull(RadioSelect):
    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None: value = ''
        str_value = force_unicode(value) # Normalize to string.
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        if choices[0][0] == '':
            choices.pop(0)
        return self.renderer(name, str_value, final_attrs, choices)
# END

QuizAttemptAnswerFormset = modelformset_factory(QuizAttemptAnswer,
                                                fields=('answer',),
                                                widgets={'answer': RadioSelectNotNull()},
                                                extra=0)
