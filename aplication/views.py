from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from users.models import User
from django.db.models import Count
from django.utils import timezone
from .forms import QuestionForm
from django.urls import reverse, reverse_lazy


class GetContextDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = context[self.context_object_name]
        questions_info = {}

        for question in questions:
            count_for = VoiceQuestion.objects.filter(question=question, status=True).count()
            count_against = VoiceQuestion.objects.filter(question=question, status=False).count()
            date_difference = timezone.now() - question.date_create
            questions_info[question.id] = {
                'question_days': date_difference.days,
                'question_hours': date_difference.seconds // 3600,
                'question_minutes': (date_difference.seconds % 3600) // 60,
                'total': count_for - count_against
            }
        context['questions_info'] = questions_info
        return context


class IndexListView(GetContextDataMixin, ListView):
    """
    Главная страница.
    """
    model = Question
    template_name = 'aplication/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.annotate(num_answers=Count('answer')).all().order_by('title')


class MyQuestionsListView(GetContextDataMixin, ListView):
    """
    Мои вопросы.
    """
    model = Question
    template_name = 'aplication/my_questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        user = self.request.user
        return Question.objects.filter(author=user)


class MyAnswersListView(ListView):
    """
    Мои Ответы.
    """
    model = Answer
    template_name = 'aplication/my_answers.html'
    context_object_name = 'answers'

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(author=user).annotate(
            answers_count=Count('question__answer')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        date_difference = timezone.now() - user.date_joined
        context['days'] = date_difference.days
        answers = context[self.context_object_name]
        questions_info = {}

        for answer in answers:
            count_for_answer = VoiceAnswer.objects.filter(answer=answer, status=True).count()
            count_against_answer = VoiceAnswer.objects.filter(answer=answer, status=False).count()
            count_for_question = VoiceQuestion.objects.filter(question=answer.question, status=True).count()
            count_against_question = VoiceQuestion.objects.filter(question=answer.question, status=False).count()
            questions_info[answer.id] = {
                'total_answers': count_for_answer - count_against_answer,
                'total_questions': count_for_question - count_against_question,
            }
        context['questions_info'] = questions_info
        return context


class TagsListView(ListView):
    """
    Страница тегов.
    """
    model = Tag
    template_name = 'aplication/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(num_questions=Count('question')).all()


class UsersListView(ListView):
    """
    Список пользователей.
    """
    model = User
    template_name = 'aplication/users.html'
    context_object_name = 'users'


class QuestionDetailView(DetailView):
    """
    Страница вопроса.
    """
    model = Question
    template_name = 'aplication/question_detail.html'
    context_object_name = 'question'

    def get_object(self, queryset=None):
        question = super().get_object(queryset)
        question.total_views()
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.object
        user = self.request.user
        questions_voice_up = VoiceQuestion.objects.filter(author=user, status=True).values_list('question', flat=True)
        questions_voice_down = VoiceQuestion.objects.filter(author=user, status=False).values_list('question', flat=True)
        context['questions_voice_up'] = questions_voice_up
        context['questions_voice_down'] = questions_voice_down
        answers = Answer.objects.filter(question=question)
        context['answers'] = answers
        context['answers_count'] = answers.count()
        count_for_question = VoiceQuestion.objects.filter(question=question, status=True).count()
        count_against_question = VoiceQuestion.objects.filter(question=question, status=False).count()
        context['voice_question_count'] = count_for_question - count_against_question
        favorite_answers = FavoritAnswer.objects.filter(author=user, status=True).values_list('answer', flat=True)
        context['favorite_answers'] = favorite_answers
        favorite_questions = FavoritQuestion.objects.filter(author=user, status=True).values_list('question', flat=True)
        context['favorite_questions'] = favorite_questions
        answers_voice_up = VoiceAnswer.objects.filter(author=user, status=True).values_list('answer', flat=True)
        answers_voice_down = VoiceAnswer.objects.filter(author=user, status=False).values_list('answer', flat=True)
        context['answers_voice_up'] = answers_voice_up
        context['answers_voice_down'] = answers_voice_down

        votes_count = {}
        for answer in answers:
            count_for = VoiceAnswer.objects.filter(answer=answer, status=True).count()
            count_against = VoiceAnswer.objects.filter(answer=answer, status=False).count()
            votes_count[answer.id] = {
                'total': count_for - count_against,
            }
        context['answer_info'] = votes_count

        return context


class UnansweredListView(GetContextDataMixin, ListView):
    """
    Страница вопросов без ответа.
    """
    model = Question
    template_name = 'aplication/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        questions = Question.objects.annotate(num_answers=Count('answer')).filter(num_answers=0)
        return questions


class FavoritesQuestionsListView(ListView):
    """
    Любимые вопросы.
    """
    model = FavoritQuestion
    template_name = 'aplication/favorite_questions.html'
    context_object_name = 'favorite_questions'

    def get_queryset(self):
        user = self.request.user
        favorite_questions = FavoritQuestion.objects.filter(author=user, status=True).annotate(num_answers=Count('question__answer'))
        return favorite_questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        date_difference = timezone.now() - user.date_joined
        context['days'] = date_difference.days
        favorite_questions = context[self.context_object_name]
        questions_info = {}

        for favorite_question in favorite_questions:
            count_for = VoiceQuestion.objects.filter(question=favorite_question.question, status=True).count()
            count_against = VoiceQuestion.objects.filter(question=favorite_question.question, status=False).count()
            questions_info[favorite_question.id] = {
                'total': count_for - count_against
            }
        context['questions_info'] = questions_info
        return context


class FavoritesAnswersListView(ListView):
    """
    Любимые ответы.
    """
    model = FavoritAnswer
    template_name = 'aplication/favorite_answers.html'
    context_object_name = 'favorite_answers'

    def get_queryset(self):
        user = self.request.user
        favorite_answers = FavoritAnswer.objects.filter(author=user, status=True).annotate(
            answers_count=Count('answer__question__answer')
        )
        return favorite_answers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        date_difference = timezone.now() - user.date_joined
        context['days'] = date_difference.days
        favorite_answers = context[self.context_object_name]
        questions_info = {}

        for favorite_answer in favorite_answers:
            count_for_answer = VoiceAnswer.objects.filter(answer=favorite_answer.answer, status=True).count()
            count_against_answer = VoiceAnswer.objects.filter(answer=favorite_answer.answer, status=False).count()
            count_for_question = VoiceQuestion.objects.filter(question=favorite_answer.answer.question, status=True).count()
            count_against_question = VoiceQuestion.objects.filter(question=favorite_answer.answer.question, status=False).count()
            questions_info[favorite_answer.id] = {
                'total_answers': count_for_answer - count_against_answer,
                'total_questions': count_for_question - count_against_question,
            }
        context['questions_info'] = questions_info
        return context


class FilterQuestionsIndexListView(GetContextDataMixin, ListView):
    """
    Фильтрация вопросов по промежутку времени.
    """
    model = Question
    template_name = 'aplication/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        pk = int(self.kwargs.get('pk'))
        days_difference = timezone.timedelta(days=pk)
        qustions = Question.objects.filter(date_create__gte=timezone.now() - days_difference).annotate(num_answers=Count('answer')).all()
        return qustions


class PopularListView(GetContextDataMixin, ListView):
    """
    Популярные вопросы.
    """
    model = Question
    template_name = 'aplication/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        questions = Question.objects.all().annotate(num_answers=Count('answer')).all().order_by('-views')
        return questions


class FilterTagsViewsListView(ListView):
    """
    Фильтрация тегов по просмотрам.
    """
    model = Tag
    template_name = 'aplication/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(num_questions=Count('question')).all().order_by('-num_questions')


class FilterTagsTitleListView(ListView):
    """
    Фильтрация тегов по имени.
    """
    model = Tag
    template_name = 'aplication/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(num_questions=Count('question')).all().order_by('title')


class FilterTagsDateListView(ListView):
    """
    Фильтрация тегов по дате.
    """
    model = Tag
    template_name = 'aplication/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(num_questions=Count('question')).all().order_by('-date_create')


def is_favorite_answer(request):
    """
    Функция - изменить статус ответа закладках.
    """
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = Answer.objects.get(id=answer_id)

        try:
            favorite = FavoritAnswer.objects.get(author=request.user, answer=answer)
            if favorite.status:
                favorite.status = False
            else:
                favorite.status = True
            favorite.save()
        except ObjectDoesNotExist:
            FavoritAnswer.objects.create(author=request.user, answer=answer, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def is_favorite_question(request):
    """
    Функция - изменить статус вопроса в закладках.
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question = Question.objects.get(id=question_id)

        try:
            favorite = FavoritQuestion.objects.get(author=request.user, question=question)
            if favorite.status:
                favorite.status = False
            else:
                favorite.status = True
            favorite.save()
        except ObjectDoesNotExist:
            FavoritQuestion.objects.create(author=request.user, question=question, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def question_voice_up(request):
    """
    Функция - изменить голос вопроса в положительную сторону.
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question = Question.objects.get(id=question_id)

        try:
            favorite = VoiceQuestion.objects.get(author=request.user, question=question)
            if favorite.status == False:
                favorite.status = None
            else:
                favorite.status = True
            favorite.save()
        except ObjectDoesNotExist:
            VoiceQuestion.objects.create(author=request.user, question=question, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def question_voice_down(request):
    """
    Функция - изменить голос вопроса в отнрицательную сторону.
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question = Question.objects.get(id=question_id)

        try:
            favorite = VoiceQuestion.objects.get(author=request.user, question=question)
            if favorite.status:
                favorite.status = None
            else:
                favorite.status = False
            favorite.save()
        except ObjectDoesNotExist:
            VoiceQuestion.objects.create(author=request.user, question=question, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def answer_voice_up(request):
    """
    Функция - изменить голос вопроса в положительную сторону.
    """
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = Answer.objects.get(id=answer_id)

        try:
            favorite = VoiceAnswer.objects.get(author=request.user, answer=answer)
            if favorite.status == False:
                favorite.status = None
            else:
                favorite.status = True
            favorite.save()
        except ObjectDoesNotExist:
            VoiceAnswer.objects.create(author=request.user, answer=answer, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def answer_voice_down(request):
    """
    Функция - изменить голос вопроса в отнрицательную сторону.
    """
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = Answer.objects.get(id=answer_id)

        try:
            favorite = VoiceAnswer.objects.get(author=request.user, answer=answer)
            if favorite.status:
                favorite.status = None
            else:
                favorite.status = False
            favorite.save()
        except ObjectDoesNotExist:
            VoiceAnswer.objects.create(author=request.user, answer=answer, status=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class QuestioCreateView(CreateView):
    """
    Создание вопроса.
    """
    models = Question
    form_class = QuestionForm
    template_name = 'aplication/create_question.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('aplication:index')


class EditQuestionUpdateView(UpdateView):
    """
    Редактирование вопроса.
    """
    model = Question
    form_class = QuestionForm
    template_name = 'aplication/create_question.html'
    success_url = reverse_lazy('aplication:index')


