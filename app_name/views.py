# app_name/views.py
import csv
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings


def load_translations():
    # Path to the CSV file
    csv_path = os.path.join(settings.BASE_DIR, 'app_name', 'translations.csv')

    # Dictionary to store translations
    translations = {}

    # Load the CSV file into a dictionary
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            czech_word = row['czech_word'].strip().lower()
            english_word = row['english_word'].strip().lower()
            translations[czech_word] = english_word

    return translations


# Load translations once when the app starts
translations_dict = load_translations()


def home(request):
    if request.method == "POST":
        input_text = request.POST.get("input_text", "").strip().lower()
        translated_words = []

        # Translate each word individually
        for word in input_text.split():
            # Use "Unknown word" if the word is not found in the translations dictionary
            translated_word = translations_dict.get(word, "Unknown word")
            translated_words.append(translated_word)

        translated_text = ' '.join(translated_words)
        return JsonResponse({"translated_text": translated_text})

    return render(request, "app_name/index.html")
