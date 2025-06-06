# findword_game/load_words.py
import csv
from findword_game.models import Word
from django.core.management.base import BaseCommand

def run():
    with open('findword_game/word_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row.get('word', '').strip().lower()
            definition = row.get('definition', '').strip()

            # Skip entries with missing word or definition
            if not word or not definition:
                continue

            Word.objects.get_or_create(word=word, defaults={'definition': definition})
