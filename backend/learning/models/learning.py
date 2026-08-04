from django.conf import settings
from django.db import models

from .vocabulary import Vocabulary


class LearnedWord(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learned_words",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="learned_by",
    )

    mastered = models.BooleanField(default=False)

    repetitions = models.PositiveIntegerField(default=0)

    interval = models.PositiveIntegerField(default=1)

    ease_factor = models.FloatField(default=2.5)

    review_date = models.DateField(
        null=True,
        blank=True,
    )

    last_reviewed = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vocabulary"],
                name="unique_learned_word",
            )
        ]

        indexes = [
            models.Index(fields=["user", "review_date", "mastered"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.simplified}"


class FavoriteWord(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorited_words",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "vocabulary"],
                name="unique_favorite_word",
            )
        ]

    def __str__(self):
        return f"{self.user.username} ❤️ {self.vocabulary.simplified}"