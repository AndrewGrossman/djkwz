from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import LessonSelectForm, QuizSelectForm, QuizAttemptAnswerFormset

from .models import *



@login_required
def home(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))

    lessons_form = LessonSelectForm()
    quizzes_form = QuizSelectForm()

    return render(request, "home.html", locals())


@login_required
def lesson(request):
    pass


@login_required
def lesson(request):
    lesson = Lesson.objects.get(pk=request.GET.get('lesson'))

    return render(request, "lesson.html", locals())

@login_required
def quiz(request):
    if request.method == 'POST':
        formset = QuizAttemptAnswerFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()

            # TODO: Give a quiz score, perhaps?
            return HttpResponseRedirect(reverse('home'))
        else:
            raise NotImplemented

    quiz = Quiz.objects.get(pk=request.GET.get('quiz', request.POST.get('quiz', None)))

    # For ease of development at this point, just order by question pk
    questions = Question.objects.filter(principles__lesson__quiz=quiz).exclude(content='').exclude(content__isnull=True)

    question_id = request.GET.get('question', request.POST.get('question', None))

    # # Initially, the plan was to get each question one at a time:
    #
    # if question_id is not None:
    #     questions = questions.filter(pk__gt=question_id)
    #
    # question = questions.first()
    #
    # if not question_id: # First time in, make a QuizAttempt for this user
    #     attempt = QuizAttempt.objects.create(user=request.user,
    #                                          quiz=quiz)
    # else:  # Otherwise, just get the latest one. Not ideal in practice, but should work.
    #     attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('created_timestamp').last()

    attempt = QuizAttempt.objects.create(user=request.user,
                                         quiz=quiz)

    # You wouldn't really want to make the object ahead of time just to leverage the ModelForm if you could help it,
    # but this will be simpler...
    for q in questions:  # TODO: Bulk create?
        answer_attempt = attempt.quizattemptanswer_set.create(question=q)

    formset = QuizAttemptAnswerFormset(queryset=attempt.quizattemptanswer_set.all())

    return render(request, "quiz.html", locals())
