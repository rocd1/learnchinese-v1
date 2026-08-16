from django.conf import settings
from django.db import models

from .curriculum import HSKLevel
from .vocabulary import Vocabulary


class QuizResult(models.Model):

    class QuizStatus(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    class QuizType(models.TextChoices):
        FLASHCARD = "flashcard", "Flashcard"
        MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
        MATCHING = "matching", "Matching"
        TYPING = "typing", "Typing"
        LISTENING = "listening", "Listening"
        DRAG_DROP = "drag_drop", "Drag & Drop"
        WORD_TILE = "word_tile", "Word Tile"

    class TypingMode(models.TextChoices):
        MEANING_TO_CHINESE = (
            "meaning_to_chinese",
            "Meaning to Chinese",
        )
        CHINESE_TO_PINYIN = (
            "chinese_to_pinyin",
            "Chinese to Pinyin",
        )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    status = models.CharField(
        max_length=20,
        choices=QuizStatus.choices,
        default=QuizStatus.IN_PROGRESS,
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

    correct_answers = models.PositiveIntegerField(
        default=0,
    )

    raw_score = models.PositiveIntegerField(
        default=0,
    )

    duration_seconds = models.PositiveIntegerField(
        default=0,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    typing_mode = models.CharField(
        max_length=30,
        choices=TypingMode.choices,
        blank=True,
    )

    class Meta:
        ordering = ["-id"]

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

    user_answer = models.CharField(
        max_length=255,
    )

    correct_answer = models.CharField(
        max_length=255,
    )

    is_correct = models.BooleanField()

    answered_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["answered_at"]

    def __str__(self):
        return (
            f"{self.quiz.user.username} "
            f"- {self.vocabulary.simplified}"
        )