from rest_framework import serializers

from learning.models import FavoriteWord, Vocabulary


# ============================================================
# FAVORITE SERIALIZER
# ============================================================

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying a user's favorite vocabulary words.
    """

    simplified = serializers.CharField(
        source="vocabulary.simplified",
        read_only=True,
    )

    pinyin = serializers.CharField(
        source="vocabulary.pinyin",
        read_only=True,
    )

    meaning = serializers.JSONField(
        source="vocabulary.meaning",
        read_only=True,
    )

    class Meta:
        model = FavoriteWord

        fields = (
            "id",
            "vocabulary",
            "simplified",
            "pinyin",
            "meaning",
            "created_at",
        )

        read_only_fields = (
            "id",
            "simplified",
            "pinyin",
            "meaning",
            "created_at",
        )


# ============================================================
# FAVORITE TOGGLE SERIALIZER
# ============================================================

class FavoriteToggleSerializer(serializers.Serializer):
    """
    Serializer for adding or removing a vocabulary word
    from the user's favorites.

    The same endpoint handles both actions:

        POST /api/favorites/toggle/
    """

    vocabulary = serializers.PrimaryKeyRelatedField(
        queryset=Vocabulary.objects.all(),
    )
