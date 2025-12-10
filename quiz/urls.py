from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, UserScoreViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='quiz-questions')

urlpatterns = [
    path('', include(router.urls)),
    path('my-score/', UserScoreViewSet.as_view({'get': 'my_score'}), name='my-score'),
    path('leaderboard/', UserScoreViewSet.as_view({'get': 'leaderboard'}), name='leaderboard'),
    path('settings/', UserScoreViewSet.as_view({'get': 'get_quiz_settings'}), name='settings'),
    path('toggle-leaderboard/', UserScoreViewSet.as_view({'post': 'toggle_leaderboard'}), name='toggle-leaderboard'),
]
