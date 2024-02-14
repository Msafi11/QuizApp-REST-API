from django.urls import path, include
from api.views import CustomUserView, CustomRegisterView, QuizCreateView, QuizDetailView, QuizSolutionView, QuizGradesBySecretKeyView


urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('signup/', CustomRegisterView.as_view(), name='rest_register'),
    path('users/', CustomUserView.as_view()),
    path('users/<int:pk>/', CustomUserView.as_view()),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/detail/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/solution/', QuizSolutionView.as_view(), name='quiz-solution'),
    path('quiz-grades/<str:secret_key>/', QuizGradesBySecretKeyView.as_view(), name='quiz_grades_by_secret_key'),
]