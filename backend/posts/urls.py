from django.urls import path

from . import views

urlpatterns = [
    path('', views.POSTS.as_view()),
    path('<int:post_id>/questions', views.QUESTIONS.as_view()),
    path('<int:post_id>/questions/<int:question_id>/replies', views.REPLIES.as_view()),
]