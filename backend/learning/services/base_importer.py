from __future__ import annotations

import logging
import time
import unicodedata
from pathlib import Path

from django.db import transaction
from django.utils.text import slugify


logger = logging.getLogger("learning.importer")


class BaseImporter:
    """
    Base class for all importers.

    Provides:

    • logging
    • timing
    • statistics
    • transactions
    • helper methods
    """

    def __init__(self, file_path: str | Path):

        self.file_path = Path(file_path)

        self.stats = {
            "processed": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
        }

        self.errors: list[str] = []


    
    def run(self):

        if not self.file_path.exists():
            raise FileNotFoundError(self.file_path)

        logger.info("Starting import: %s", self.file_path)

        start = time.perf_counter()

        with transaction.atomic():

            
            self.import_data()

        seconds = round(time.perf_counter() - start, 2)

        logger.info("Import completed in %.2f seconds", seconds)

        return {
            **self.stats,
            "seconds": seconds,
            "errors": self.errors,
        }

    @staticmethod
    def clean_text(value):

        if value is None:
            return ""

        return unicodedata.normalize("NFKC", str(value)).strip()

    @staticmethod
    def normalize_pinyin(text):

        if not text:
            return ""

        text = unicodedata.normalize("NFD", text)

        text = "".join(
            c
            for c in text
            if unicodedata.category(c) != "Mn"
        )

        return text.replace("ü", "v").replace(" ", "").lower()

    @staticmethod
    def create_slug(text):

        return slugify(text)

    def update_or_create(
        self,
        model,
        lookup,
        defaults,
    ):

        _, created = model.objects.update_or_create(
            **lookup,
            defaults=defaults,
        )

        if created:
            self.stats["created"] += 1
        else:
            self.stats["updated"] += 1

    def skip(self, reason):

        self.stats["skipped"] += 1

        logger.warning(reason)

    def error(self, reason):

        self.stats["errors"] += 1

        self.errors.append(reason)

        logger.exception(reason)

    def print_summary(self):

        logger.info("=" * 60)

        logger.info("Processed : %s", self.stats["processed"],)

        logger.info("Created : %s", self.stats["created"])

        logger.info("Updated : %s", self.stats["updated"])

        logger.info("Skipped : %s", self.stats["skipped"])

        logger.info("Errors  : %s", self.stats["errors"])

        logger.info("=" * 60)