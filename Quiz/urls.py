from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quiz/<int:quiz_id>/', views.take_quiz_view, name='take_quiz'),
    path('quiz/create/', views.create_quiz_view, name='create_quiz'),
    path(
        'quiz/<int:quiz_id>/add-question/',
        views.add_question_view,
        name='add_question',
    ),
]