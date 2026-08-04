from django.db import models


# ============================================================
# HSK LEVEL
# ============================================================

class HSKLevel(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    level = models.PositiveSmallIntegerField(
        unique=True,
    )

    total_words = models.PositiveIntegerField(
        default=0,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="hsk_levels/",
        blank=True,
        null=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["level"]
        verbose_name = "HSK Level"
        verbose_name_plural = "HSK Levels"

    def __str__(self):
        return self.name


# ============================================================
# LESSON
# ============================================================

class Lesson(models.Model):

    hsk_level = models.ForeignKey(
        HSKLevel,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = [
            "hsk_level",
            "order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["hsk_level", "order"],
                name="unique_lesson_order_per_hsk",
            )
        ]

    def __str__(self):
        return self.title