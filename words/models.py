from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class Word(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    synonyms = models.TextField(blank=True)
    antonyms = models.TextField(blank=True)
    example = models.TextField(blank=True)
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.word

class SavedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'word']
