from rest_framework import serializers

from learning.models import (
    QuizAnswer,
    QuizResult,
)

from .vocabulary import VocabularyListSerializer


class QuizAnswerSerializer(serializers.ModelSerializer):

    vocabulary = VocabularyListSerializer(
        read_only=True,
    )

    class Meta:
        model = QuizAnswer
        fields = (
            "id",
            "vocabulary",
            "user_answer",
            "correct_answer",
            "is_correct",
            "answered_at",
        )


class QuizResultSerializer(serializers.ModelSerializer):

    answers = QuizAnswerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = QuizResult
        fields = (
            "id",
            "quiz_type",
            "hsk_level",
            "total_questions",
            "correct_answers",
            "raw_score",
            "duration_seconds",
            "completed_at",
            "answers",
        )