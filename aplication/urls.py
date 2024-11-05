from django.urls import path
from . import views
from .views import *


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
    # Все пользователи
    path('users/', views.UsersListView.as_view(), name='users'),
    # Конкретный вопрос
    path('question/<pk>/', views.QuestionDetailView.as_view(), name='detail_question'),
    # Неотвеченные вопросы
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
    path('create_question/', views.QuestionCreateView.as_view(), name='create_question'),
    # Url создать ответ
    path('question/<int:question_id>/answer/create/', views.AnswerCreateView.as_view(), name='create_answer'),
    # Url редактировать вопрос
    path('<int:pk>/edit/question/', views.EditQuestionUpdateView.as_view(), name='edit'),
    # Url редактировать ответ
    path('<int:pk>/edit/answer/', views.EditAnswerUpdateView.as_view(), name='edit_answer'),
    # Url мои комментарии
    path('my_comments/', views.MyComments.as_view(), name='comments'),
    # Url Функция 'Принять вопрос'
    path('make_question_accepted/', make_question_accepted, name='make_question_accepted'),
    # Url создать комментарий к вопросу
    path('question/<int:question_id>/comment/create/', views.CommentCreateView.as_view(), name='create_comment_question'),
    # Url создать комментарий к ответу
    path('answers/<int:answer_id>/comments/create/', views.CommentCreateView.as_view(), name='create_comment_answer'),
    # Url редактировать комментарий
    path('<int:pk>/edit/comment/', views.EditCommentUpdateView.as_view(), name='edit_comment'),
    # Url удалить комментарий
    path('<int:pk>/delete/comment/', delete_comment, name='delete_comment'),
    # Url удалить ответ
    path('<int:pk>/delete/answer/', delete_answer, name='delete_answer'),
    # Вопросы по тегу
    path('<slug:slug>/questions/', views.IndexTagsListView.as_view(), name='questions_tag'),
    # Поиск вопроса
    path('search_question/', views.SearchQuestionListView.as_view(), name='search_question'),
    # Поиск вопроса
    path('search_tag/', views.SearchTagListView.as_view(), name='search_tag'),
    # Url загрузки аватара
    path('upload_user_image/', upload_user_image, name='upload_user_image'),
    # Url загрузки Telegram ID
    path('post_telegram_id/', post_telegram_id, name='post_telegram_id'),
]
