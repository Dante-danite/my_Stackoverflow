from django.urls import include, path
from rest_framework import routers
import api.views

router_v1 = routers.SimpleRouter()
router_v1.register('questions', api.views.QuestionViewSet)
router_v1.register('answers', api.views.AnswerViewSet)
router_v1.register('comments', api.views.CommentViewSet)
router_v1.register('tags', api.views.TagViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]