import csv
from django.core.management.base import BaseCommand
from findword_game.models import Word

class Command(BaseCommand):
    help = 'Load words and definitions from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    word_text = row.get('word', '').strip()
                    definition = row.get('definition', '').strip()
                    
                    if word_text and definition:
                        Word.objects.get_or_create(word=word_text, definition=definition)
                        count += 1
                
                self.stdout.write(self.style.SUCCESS(f"✅ Loaded {count} words into the database."))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"❌ File not found: {csv_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error loading CSV: {e}"))
