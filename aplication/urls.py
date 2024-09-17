from django.urls import path
from . import views
from .views import is_favorite_answer, is_favorite_question, question_voice_up, question_voice_down, answer_voice_up, answer_voice_down

app_name = 'aplication'

urlpatterns = [
    # Главная страница
    path('', views.IndexListView.as_view(), name='index'),
    # Мои вопросы
    path('my_questions/', views.MyQuestionsListView.as_view(), name='my_questions'),
    # Мои ответы
    path('my_answers/', views.MyAnswersListView.as_view(), name='my_answers'),
    # Все теги
    path('tags/', views.TagsListView.as_view(), name='tags'),
    # Все пользоваетли
    path('users/', views.UsersListView.as_view(), name='users'),
    # Конретный вопрос
    path('question/<pk>/', views.QuestionDetailView.as_view(), name='detail_question'),
    # Неотвеченые вопросы
    path('unanswered/', views.UnansweredListView.as_view(), name='unanswered'),
    # Любимые вопросы
    path('favorites_questions/', views.FavoritesQuestionsListView.as_view(), name='favorites_questions'),
    # Любимые ответы
    path('favorites_answers/', views.FavoritesAnswersListView.as_view(), name='favorites_answers'),
    # Фильтрация вопросов по дням
    path('question_days/<pk>/', views.FilterQuestionsIndexListView.as_view(), name='qustion_days'),
    # Популярные вопросы
    path('popular_questions/', views.PopularListView.as_view(), name='popular_questions'),
    # Фильтрация тегов по кол-ву вопросов
    path('popular_tags/', views.FilterTagsViewsListView.as_view(), name='popular_tags'),
    # Фильтрация тегов по алфавиту
    path('tags_name/', views.FilterTagsTitleListView.as_view(), name='tags_name'),
    # Фильтрация тегов дате
    path('tags_date/', views.FilterTagsDateListView.as_view(), name='tags_date'),
    # Url изменения статуса вопроса в закладках
    path('is_favorite_answer/', is_favorite_answer, name='is_favorite_answer'),
    # Url изменения статуса вопроса в закладках
    path('is_favorite_question/', is_favorite_question, name='is_favorite_question'),
    # Url изменения голоса вопроса в положительную сторону
    path('question_voice_up/', question_voice_up, name='question_voice_up'),
    # Url изменения голоса вопроса в отрицательную сторону
    path('question_voice_down/', question_voice_down, name='question_voice_down'),
    # Url изменения голоса ответа в положительную сторону
    path('answer_voice_up/', answer_voice_up, name='answer_voice_up'),
    # Url изменения голоса ответа в отрицательную сторону
    path('answer_voice_down/', answer_voice_down, name='answer_voice_down'),
    # Url создать вопрос
    path('create_question/', views.QuestioCreateView.as_view(), name='create_question'),
    # Url редактировать вопрос
    path('<int:pk>/edit/', views.EditQuestionUpdateView.as_view(), name='edit'),
]
