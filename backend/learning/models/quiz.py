from django.conf import settings
from django.db import models

from .curriculum import HSKLevel
from .vocabulary import Vocabulary


class QuizResult(models.Model):

    class QuizType(models.TextChoices):
        FLASHCARD = "flashcard", "Flashcard"
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
        MATCHING = "matching", "Matching"
        TYPING = "typing", "Typing"
        LISTENING = "listening", "Listening"
        DRAG_DROP = "drag_drop", "Drag & Drop"
        WORD_TILE = "word_tile", "Word Tile"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    quiz_type = models.CharField(
        max_length=30,
        choices=QuizType.choices,
    )

    hsk_level = models.ForeignKey(
        HSKLevel,
        on_delete=models.PROTECT,
        related_name="quiz_results",
    )

    total_questions = models.PositiveIntegerField()

    correct_answers = models.PositiveIntegerField()

    raw_score = models.PositiveIntegerField()

    duration_seconds = models.PositiveIntegerField()

    completed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type}"


class QuizAnswer(models.Model):

    quiz = models.ForeignKey(
        QuizResult,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    vocabulary = models.ForeignKey(
        Vocabulary,
        on_delete=models.CASCADE,
        related_name="quiz_answers",
    )

    user_answer = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=255)

    is_correct = models.BooleanField()

    answered_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["answered_at"]

    def __str__(self):
        return f"{self.quiz.user.username} - {self.vocabulary.simplified}"