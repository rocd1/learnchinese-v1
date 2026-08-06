from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from learning.services.vocabulary_importer import VocabularyImporter


class Command(BaseCommand):

    help = "Import HSK vocabulary"

    def add_arguments(self, parser):

        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing vocabulary first.",
        )

    def handle(self, *args, **options):

        from learning.models import Vocabulary

        if options["clear"]:

            Vocabulary.objects.all().delete()

            self.stdout.write(
                self.style.WARNING(
                    "Existing vocabulary deleted."
                )
            )

        importer = VocabularyImporter(

            Path(settings.BASE_DIR)
            / "data"
            / "json"
            / "hsk.json"

        )

        stats = importer.run()

        self.stdout.write(

            self.style.SUCCESS(

                f"""
Import Complete

Processed : {stats['created']}
Created : {stats['created']}
Updated : {stats['updated']}
Skipped : {stats['skipped']}
Errors  : {stats['errors']}
Time    : {stats['seconds']} seconds
"""

            )

        )