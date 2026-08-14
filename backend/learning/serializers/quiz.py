from rest_framework import serializers

from learning.models import (
    HSKLevel,
    QuizAnswer,
    QuizResult,
    Vocabulary,
)

from .vocabulary import VocabularyListSerializer



# ============================================================
# QUIZ ANSWER
# ============================================================


class QuizAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for an individual answer inside a quiz.
    """

    vocabulary = VocabularyListSerializer(
        read_only=True,
    )

    vocabulary_id = serializers.PrimaryKeyRelatedField(
        source="vocabulary",
        queryset=Vocabulary.objects.all(),
        write_only=True,
    )

    class Meta:
        model = QuizAnswer

        fields = (
            "id",
            "vocabulary",
            "vocabulary_id",
            "user_answer",
            "correct_answer",
            "is_correct",
            "answered_at",
        )

        read_only_fields = (
            "id",
            "vocabulary",
            "correct_answer",
            "is_correct",
            "answered_at",
        )


# ============================================================
# QUIZ RESULT
# ============================================================


class QuizResultSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz results and quiz history.
    """

    quiz_type_display = serializers.CharField(
        source="get_quiz_type_display",
        read_only=True,
    )

    typing_mode_display = serializers.CharField(
        source="get_typing_mode_display",
        read_only=True,
    )

    hsk_level = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    hsk_level_name = serializers.CharField(
        source="hsk_level.name",
        read_only=True,
    )

    answers = QuizAnswerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = QuizResult

        fields = (
            "id",
            "quiz_type",
            "quiz_type_display",
            "typing_mode",
            "typing_mode_display",
            "hsk_level",
            "hsk_level_name",
            "total_questions",
            "correct_answers",
            "raw_score",
            "duration_seconds",
            "completed_at",
            "answers",
        )

        read_only_fields = fields


# ============================================================
# START QUIZ
# ============================================================


class QuizStartSerializer(serializers.Serializer):
    """
    Validate a request to start a quiz.
    """

    quiz_type = serializers.ChoiceField(
        choices=QuizResult.QuizType.choices,
    )

    hsk_level = serializers.PrimaryKeyRelatedField(
        queryset=HSKLevel.objects.all(),
    )

    total_questions = serializers.IntegerField(
        min_value=1,
        max_value=50,
    )

    typing_mode = serializers.ChoiceField(
        choices=QuizResult.TypingMode.choices,
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        """
        typing_mode is only valid for typing quizzes.
        """

        quiz_type = attrs["quiz_type"]

        typing_mode = attrs.get(
            "typing_mode",
            "",
        )

        if (
            quiz_type == QuizResult.QuizType.TYPING
            and not typing_mode
        ):
            raise serializers.ValidationError(
                {
                    "typing_mode": (
                        "This field is required for typing quizzes."
                    )
                }
            )

        if (
            quiz_type != QuizResult.QuizType.TYPING
            and typing_mode
        ):
            raise serializers.ValidationError(
                {
                    "typing_mode": (
                        "typing_mode can only be used "
                        "with typing quizzes."
                    )
                }
            )

        return attrs


# ============================================================
# SUBMIT ANSWER
# ============================================================


class QuizAnswerSubmitSerializer(serializers.Serializer):
    """
    Validate a user's answer to a quiz question.
    """

    vocabulary = serializers.PrimaryKeyRelatedField(
        queryset=Vocabulary.objects.all(),
    )

    user_answer = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )


# ============================================================
# COMPLETE QUIZ
# ============================================================


class QuizCompleteSerializer(serializers.Serializer):
    """
    Validate completion information for a quiz.
    """

    duration_seconds = serializers.IntegerField(
        min_value=0,
    )