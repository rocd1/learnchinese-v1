from rest_framework import serializers


class DashboardStatisticsSerializer(serializers.Serializer):
    """
    Serializer for dashboard summary statistics.
    """

    total_words = serializers.IntegerField()

    words_learned = serializers.IntegerField()

    words_mastered = serializers.IntegerField()

    words_in_progress = serializers.IntegerField()

    favorites = serializers.IntegerField()

    quizzes_completed = serializers.IntegerField()

    due_for_review = serializers.IntegerField()