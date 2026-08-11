from rest_framework import serializers

from learning.models import (
    FavoriteWord,
    LearnedWord,
    Vocabulary,
)

from .vocabulary import VocabularyListSerializer


class LearnedWordSerializer(serializers.ModelSerializer):
    """
    Display a user's learning progress for a vocabulary word.
    """

    vocabulary = VocabularyListSerializer(
        read_only=True,
    )

    class Meta:
        model = LearnedWord
        fields = (
            "id",
            "vocabulary",
            "mastered",
            "repetitions",
            "interval",
            "ease_factor",
            "review_date",
            "last_reviewed",
            "created_at",
            "updated_at",
        )


class FavoriteWordSerializer(serializers.ModelSerializer):
    """
    Display a user's favorite vocabulary words.
    """

    vocabulary = VocabularyListSerializer(
        read_only=True,
    )

    class Meta:
        model = FavoriteWord
        fields = (
            "id",
            "vocabulary",
            "created_at",
        )



class LearningSessionAnswerSerializer(serializers.Serializer):
    """
    Record the result of a learning session.
    """

    vocabulary = serializers.PrimaryKeyRelatedField(
        queryset=Vocabulary.objects.all(),
    )

    correct = serializers.BooleanField(
        default=True,
    )