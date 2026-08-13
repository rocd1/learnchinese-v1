from __future__ import annotations

from django.utils import timezone

from learning.models import (
    FavoriteWord,
    LearnedWord,
    QuizResult,
    Vocabulary,
)


class DashboardService:
    """
    Business logic for generating user dashboard statistics.
    """

    @staticmethod
    def get_statistics(user) -> dict:
        """
        Return summary statistics for the authenticated user.
        """

        today = timezone.localdate()

        # ========================================================
        # VOCABULARY
        # ========================================================

        total_words = Vocabulary.objects.count()

        # ========================================================
        # LEARNING PROGRESS
        # ========================================================

        learned_words = LearnedWord.objects.filter(
            user=user,
        )

        words_learned = learned_words.count()

        words_mastered = learned_words.filter(
            mastered=True,
        ).count()

        words_in_progress = learned_words.filter(
            mastered=False,
        ).count()

        due_for_review = learned_words.filter(
            mastered=False,
            review_date__lte=today,
        ).count()

        # ========================================================
        # FAVORITES
        # ========================================================

        favorites = FavoriteWord.objects.filter(
            user=user,
        ).count()

        # ========================================================
        # QUIZ RESULTS
        # ========================================================

        quizzes_completed = QuizResult.objects.filter(
            user=user,
        ).count()

        # ========================================================
        # RETURN STATISTICS
        # ========================================================

        return {
            "total_words": total_words,
            "words_learned": words_learned,
            "words_mastered": words_mastered,
            "words_in_progress": words_in_progress,
            "favorites": favorites,
            "quizzes_completed": quizzes_completed,
            "due_for_review": due_for_review,
        }