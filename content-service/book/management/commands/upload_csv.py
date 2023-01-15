from django.core.management import BaseCommand
from book.models import Book
import csv
from pathlib import Path

class Command(BaseCommand):
	help = 'create book instances in database by uploading a csv file'

	def add_arguments(self, parser) -> None:
		parser.add_argument('csv_file_path', type=str, help='csv file from where the data should be uploaded to database')
		return super().add_arguments(parser)

	def handle(self, *args, **options):
		file_path = Path(options['csv_file_path'])
		if not file_path.is_file() and file_path.suffix != '.csv':
			self.stderr.write(self.style.ERROR('the given path \'%s\' is not a valid csv file path'% (options['csv_file_path'])))
			return
		try:
			book_instances = []
			with open(file_path.resolve(), 'r') as file:
				reader = csv.reader(file)
				for row in reader:
					instance = Book(title=row[0], author=row[1], description=row[2], story=row[3])
					book_instances.append(instance)

			Book.objects.bulk_create(book_instances)
		except csv.Error as e:
			self.stderr.write(self.style.ERROR(e))
		except Exception as e:
			self.stderr.write(self.style.ERROR(e))
		else:
			self.stdout.write(self.style.SUCCESS('\n%s instances created succesfully\n'% (len(book_instances))))
