from rest_framework import serializers

from learning.models import (
    FavoriteWord,
    LearnedWord,
)

from .vocabulary import VocabularyListSerializer


class LearnedWordSerializer(serializers.ModelSerializer):

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
        )


class FavoriteWordSerializer(serializers.ModelSerializer):

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