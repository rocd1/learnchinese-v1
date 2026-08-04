from django.db import models

from .curriculum import HSKLevel, Lesson


# ============================================================
# VOCABULARY
# ============================================================

class Vocabulary(models.Model):

    hsk_level = models.ForeignKey(
        HSKLevel,
        on_delete=models.PROTECT,
        related_name="words",
    )

    hsk_id = models.PositiveIntegerField(
        db_index=True,
    )

    simplified = models.CharField(
        max_length=50,
        db_index=True,
    )

    traditional = models.CharField(
        max_length=50,
        blank=True,
    )

    pinyin = models.CharField(
        max_length=100,
        db_index=True,
    )

    pinyin_plain = models.CharField(
        max_length=100,
        db_index=True,
    )

    meaning = models.JSONField(
        default=list,
    )

    notes = models.TextField(
        blank=True,
    )

    audio = models.FileField(
        upload_to="vocabulary/audio/",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )

    lessons = models.ManyToManyField(
        Lesson,
        blank=True,
        related_name="vocabulary",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "hsk_level__level",
            "hsk_id",
        ]

        indexes = [
            models.Index(fields=["hsk_level"]),
            models.Index(fields=["simplified"]),
            models.Index(fields=["traditional"]),
            models.Index(fields=["pinyin"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["hsk_level", "hsk_id"],
                name="unique_vocab_per_level",
            ),
        ]

    def __str__(self):
        return f"{self.simplified} ({self.pinyin})"


# ============================================================
# EXAMPLE SENTENCE
# ============================================================

class ExampleSentence(models.Model):

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="examples",
    )

    sentence = models.TextField()

    pinyin = models.TextField()

    translation = models.TextField()

    order = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "vocabulary",
            "order",
        ]

    def __str__(self):
        return self.sentence[:50]


# ============================================================
# GRAMMAR
# ============================================================

class GrammarPoint(models.Model):

    hsk_level = models.ForeignKey(
        HSKLevel,
        on_delete=models.CASCADE,
        related_name="grammar_points",
    )

    title = models.CharField(
        max_length=200,
    )

    explanation = models.TextField(
        blank=True,
    )

    lessons = models.ManyToManyField(
        Lesson,
        blank=True,
        related_name="grammar_points",
    )

    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = [
            "hsk_level",
            "order",
        ]

    def __str__(self):
        return self.title


# ============================================================
# CHARACTER
# ============================================================

class Character(models.Model):

    hanzi = models.CharField(
        max_length=1,
        unique=True,
    )

    hsk_level = models.ForeignKey(
        HSKLevel,
        on_delete=models.CASCADE,
        related_name="characters",
    )

    practice_writing = models.BooleanField(
        default=False,
    )

    order = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "hsk_level",
            "order",
        ]

    def __str__(self):
        return self.hanzi