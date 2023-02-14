from csv import DictReader
from django.core.management import BaseCommand
from rest_api.models import Netlify
from pytz import UTC
import logging

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

logging.basicConfig(level="INFO")

class Command(BaseCommand):

    # Show this when the user types help
    help = "Loads data from csv"


    def loadFromCSV(self, csvFile):
        logging.info(f"Loading data from {csvFile}")

        for count, row in enumerate(DictReader(open(csvFile))):

            netlify = Netlify()

            logging.debug(f"Import row {count}")

            if any(row[key] in (None, "") for key in row):
                logging.warning(f"Row {row} contains empty cell")
            
            if len(row['genetic']) > 0:
                netlify.genetic = row['genetic']

            if len(row['length']) > 0:
                netlify.length = row['length']
            
            if len(row['mass']) > 0:
                netlify.mass = row['mass']

            if len(row['exercise']) > 0:
                netlify.exercise = row['exercise']

            if len(row['smoking']) > 0:
                netlify.smoking = row['smoking']

            if len(row['alcohol']) > 0:
                netlify.alcohol = row['alcohol']

            if len(row['sugar']) > 0:
                netlify.sugar = row['sugar']

            if len(row['lifespan']) > 0:
                netlify.lifespan = row['lifespan']
            
            netlify.save()
            

    def handle(self, *args, **options):

        if Netlify.objects.exists():
            logging.warning('netlify data already loaded...exiting.')
            logging.warning(ALREADY_LOADED_ERROR_MESSAGE)
            
            return

        self.loadFromCSV('data/newdata.csv')
        self.loadFromCSV('data/webscrapedata.csv')
                