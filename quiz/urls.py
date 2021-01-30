from django.urls import path, re_path
from quiz.api import MyQuizListAPI, QuizListAPI, QuizDetailAPI, SaveUsersAnswer, SubmitQuizAPI, QuizLeaderBoardAPI, UserVerificationView, tes12t
from rest_framework import routers
app_name = 'quiz'

urlpatterns = [
	path("verification2/", tes12t),
	path("my-quizzes/", MyQuizListAPI.as_view()),
	path("quizzes/", QuizListAPI.as_view()),
	path("save-answer/", SaveUsersAnswer.as_view()),
	re_path(r"quizzes/(?P<slug>[\w\-]+)/$", QuizDetailAPI.as_view()),
	re_path(r"quizzes/(?P<slug>[\w\-]+)/leaderboard/$", QuizLeaderBoardAPI.as_view()),
	re_path(r"quizzes/(?P<slug>[\w\-]+)/submit/$", SubmitQuizAPI.as_view()),
]


router = routers.DefaultRouter()
router.register('verification', UserVerificationView, basename='userverification')


urlpatterns += router.urls