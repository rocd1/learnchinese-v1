import json

from learning.models import HSKLevel, Vocabulary
from learning.services.base_importer import BaseImporter


class VocabularyImporter(BaseImporter):

    def import_data(self):

        with open(self.file_path, encoding="utf-8") as file:
            rows = json.load(file)

        level_cache = {}

        for row in rows:

            try:

                level = int(row["level"])

                if level not in level_cache:

                    level_cache[level], _ = HSKLevel.objects.get_or_create(
                        level=level,
                        defaults={
                            "name": f"HSK {level}",
                        },
                    )

                hsk_level = level_cache[level]

                simplified = self.clean_text(row["hanzi"])

                pinyin = self.clean_text(row["pinyin"])

                translations = row.get(
                    "translations",
                    [],
                )


                slug = f"hsk{level}-{row['id']}-{self.normalize_pinyin(pinyin)}"


                self.update_or_create(

                    Vocabulary,

                    lookup={
                        "hsk_level": hsk_level,
                        "hsk_id": row["id"],
                    },

                    defaults={

                        "simplified": simplified,

                        "traditional": "",

                        "pinyin": pinyin,

                        "pinyin_plain":
                            self.normalize_pinyin(
                                pinyin
                            ),

                        "meaning": translations,

                        "slug": slug,

                    },

                )

            except Exception as exc:

                self.error(
                    f"{row.get('hanzi')} : {exc}"
                )

        self.print_summary()