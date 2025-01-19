from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_of_the_day, name='word_of_day'),
    path('lookup/', views.word_lookup, name='word_lookup'),
    path('save/<int:word_id>/', views.save_word, name='save_word'),
    path('saved/', views.saved_words, name='saved_words'),
    path('quiz/', views.vocabulary_quiz, name='quiz'),
]