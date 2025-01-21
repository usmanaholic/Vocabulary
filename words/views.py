

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json
from datetime import datetime
from .models import Word, SavedWord
import random

def get_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        definition = data['meanings'][0]['definitions'][0]['definition']
        example = data['meanings'][0]['definitions'][0].get('example', '')
        synonyms = data['meanings'][0].get('synonyms', [])
        antonyms = data['meanings'][0].get('antonyms', [])
        return {
            'word': word,
            'definition': definition,
            'example': example,
            'synonyms': ', '.join(synonyms),
            'antonyms': ', '.join(antonyms)
        }
    return None

def word_of_the_day(request):
    today = datetime.now().date()
    word = Word.objects.filter(date_added=today).first()
    
    if not word:
        # List of common English words to choose from
        common_words = ['aberration', 'benevolent', 'cacophony', 'dubious', 'ephemeral']
        random_word = random.choice(common_words)
        details = get_word_details(random_word)
        
        if details:
            word = Word.objects.create(
                word=details['word'],
                definition=details['definition'],
                example=details['example'],
                synonyms=details['synonyms'],
                antonyms=details['antonyms'],
                date_added=today
            )
        else:
            # Debug information
            print(f"Failed to get details for word: {random_word}")

    # Debug information
    print(f"Word of the day: {word.word if word else 'None'}")

    return render(request, 'word_of_day.html', {'word': word})

def word_lookup(request):
    word = request.GET.get('word', '')
    if word:
        details = get_word_details(word)
        if details:
            return JsonResponse(details)
    return JsonResponse({'error': 'Word not found'})

@login_required
def save_word(request, word_id):
    word = Word.objects.get(id=word_id)
    SavedWord.objects.get_or_create(user=request.user, word=word)
    return redirect('word_of_day')

@login_required
def saved_words(request):
    saved = SavedWord.objects.filter(user=request.user).select_related('word')
    return render(request, 'saved_words.html', {'saved_words': saved})

def vocabulary_quiz(request):
    saved_words = Word.objects.all().order_by('?')[:5]
    quiz_data = []
    
    for word in saved_words:
        quiz_data.append({
            'word': word.word,
            'definition': word.definition,
            'example': word.example.replace(word.word, '_____')
        })
    

    return render(request, 'quiz.html', {'quiz_data': quiz_data})


from django.http import HttpResponse

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Render the 'home.html' template

