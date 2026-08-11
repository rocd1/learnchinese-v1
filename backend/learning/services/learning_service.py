from __future__ import annotations

import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from learning.models import LearnedWord, Vocabulary


logger = logging.getLogger("learning.learning")


class LearningService:
    """
    Business logic for vocabulary learning.

    Responsibilities:

    • Build learning sessions.
    • Select words due for review.
    • Select new words.
    • Record correct/incorrect answers.
    • Update repetitions.
    • Update review intervals.
    • Update ease factor.
    • Determine mastery.
    """

    # ============================================================
    # CONFIGURATION
    # ============================================================

    DEFAULT_SESSION_SIZE = 20

    MIN_SESSION_SIZE = 1

    MAX_SESSION_SIZE = 100

    MIN_EASE_FACTOR = 1.3

    MAX_EASE_FACTOR = 3.0

    INITIAL_EASE_FACTOR = 2.5

    MASTERY_REPETITIONS = 5

    MASTERY_EASE_FACTOR = 2.5

    # ============================================================
    # SESSION
    # ============================================================

    @staticmethod
    def get_session(
        user,
        limit: int = DEFAULT_SESSION_SIZE,
    ) -> list[Vocabulary]:
        """
        Return vocabulary for the user's learning session.

        Priority:

        1. Words that are due for review.
        2. New words the user has never studied.

        The service returns Vocabulary objects.
        Serialization is handled by the API layer.
        """

        limit = max(
            LearningService.MIN_SESSION_SIZE,
            min(
                limit,
                LearningService.MAX_SESSION_SIZE,
            ),
        )

        today = timezone.localdate()

        # --------------------------------------------------------
        # WORDS DUE FOR REVIEW
        # --------------------------------------------------------

        learned_due = (
            LearnedWord.objects
            .filter(
                user=user,
                mastered=False,
                review_date__lte=today,
            )
            .select_related(
                "vocabulary",
                "vocabulary__hsk_level",
            )
            .order_by(
                "review_date",
                "id",
            )[:limit]
        )

        due_words = [
            learned.vocabulary
            for learned in learned_due
        ]

        # --------------------------------------------------------
        # NEW WORDS
        # --------------------------------------------------------

        remaining = limit - len(due_words)

        if remaining <= 0:
            return due_words

        learned_word_ids = (
            LearnedWord.objects
            .filter(
                user=user,
            )
            .values_list(
                "vocabulary_id",
                flat=True,
            )
        )

        vocabulary_queryset = Vocabulary.objects.select_related(
            "hsk_level",
        )

        # --------------------------------------------------------
        # CURRENT HSK
        # --------------------------------------------------------

        current_hsk = getattr(
            user,
            "current_hsk",
            None,
        )

        if current_hsk:
            vocabulary_queryset = vocabulary_queryset.filter(
                hsk_level=current_hsk,
            )

        # --------------------------------------------------------
        # GET NEW WORDS
        # --------------------------------------------------------

        new_words = list(
            vocabulary_queryset
            .exclude(
                id__in=learned_word_ids,
            )
            .order_by(
                "hsk_id",
                "id",
            )[:remaining]
        )

        return due_words + new_words

    # ============================================================
    # RECORD ANSWER
    # ============================================================

    @staticmethod
    @transaction.atomic
    def record_answer(
        user,
        vocabulary: Vocabulary,
        correct: bool,
    ) -> LearnedWord:
        """
        Record the user's answer for a vocabulary word.

        Correct answer:

            • increases repetitions
            • increases review interval
            • increases ease factor
            • may mark the word as mastered

        Incorrect answer:

            • resets interval to one day
            • decreases ease factor
            • removes mastery

        A word becomes mastered when:

            repetitions >= 5

        AND:

            ease_factor >= 2.5
        """

        learned_word, created = (
            LearnedWord.objects
            .select_for_update()
            .get_or_create(
                user=user,
                vocabulary=vocabulary,
                defaults={
                    "ease_factor": (
                        LearningService.INITIAL_EASE_FACTOR
                    ),
                },
            )
        )

        now = timezone.now()

        if created:
            logger.info(
                "Started learning word: "
                "user=%s vocabulary=%s",
                user.pk,
                vocabulary.pk,
            )

        # ========================================================
        # CORRECT ANSWER
        # ========================================================

        if correct:

            learned_word.repetitions += 1

            # ----------------------------------------------------
            # REVIEW INTERVAL
            # ----------------------------------------------------

            if learned_word.repetitions == 1:

                learned_word.interval = 1

            elif learned_word.repetitions == 2:

                learned_word.interval = 3

            else:

                learned_word.interval = max(
                    1,
                    round(
                        learned_word.interval
                        * learned_word.ease_factor,
                    ),
                )

            # ----------------------------------------------------
            # EASE FACTOR
            # ----------------------------------------------------

            old_ease_factor = learned_word.ease_factor

            learned_word.ease_factor = min(
                learned_word.ease_factor + 0.1,
                LearningService.MAX_EASE_FACTOR,
            )

            if (
                learned_word.ease_factor
                == LearningService.MAX_EASE_FACTOR
                and old_ease_factor
                < LearningService.MAX_EASE_FACTOR
            ):
                logger.debug(
                    "Ease factor reached maximum: "
                    "user=%s vocabulary=%s ease_factor=%.2f",
                    user.pk,
                    vocabulary.pk,
                    learned_word.ease_factor,
                )

            # ----------------------------------------------------
            # MASTERY
            # ----------------------------------------------------

            if (
                learned_word.repetitions
                >= LearningService.MASTERY_REPETITIONS
                and learned_word.ease_factor
                >= LearningService.MASTERY_EASE_FACTOR
            ):
                learned_word.mastered = True

                logger.info(
                    "Vocabulary mastered: "
                    "user=%s vocabulary=%s",
                    user.pk,
                    vocabulary.pk,
                )

            # ----------------------------------------------------
            # NEXT REVIEW
            # ----------------------------------------------------

            learned_word.review_date = (
                now.date()
                + timedelta(
                    days=learned_word.interval,
                )
            )

        # ========================================================
        # INCORRECT ANSWER
        # ========================================================

        else:

            learned_word.mastered = False

            # Reset review interval.
            learned_word.interval = 1

            # Review again tomorrow.
            learned_word.review_date = (
                now.date()
                + timedelta(days=1)
            )

            # ----------------------------------------------------
            # DECREASE EASE FACTOR
            # ----------------------------------------------------

            old_ease_factor = learned_word.ease_factor

            learned_word.ease_factor = max(
                learned_word.ease_factor - 0.2,
                LearningService.MIN_EASE_FACTOR,
            )

            if (
                learned_word.ease_factor
                == LearningService.MIN_EASE_FACTOR
                and old_ease_factor
                > LearningService.MIN_EASE_FACTOR
            ):
                logger.debug(
                    "Ease factor reached minimum: "
                    "user=%s vocabulary=%s ease_factor=%.2f",
                    user.pk,
                    vocabulary.pk,
                    learned_word.ease_factor,
                )

            logger.info(
                "Incorrect vocabulary answer: "
                "user=%s vocabulary=%s",
                user.pk,
                vocabulary.pk,
            )

        # ========================================================
        # COMMON FIELDS
        # ========================================================

        learned_word.last_reviewed = now

        learned_word.save(
            update_fields=[
                "mastered",
                "repetitions",
                "interval",
                "ease_factor",
                "review_date",
                "last_reviewed",
                "updated_at",
            ],
        )

        logger.debug(
            "Learning progress updated: "
            "user=%s vocabulary=%s repetitions=%s "
            "interval=%s ease_factor=%.2f mastered=%s",
            user.pk,
            vocabulary.pk,
            learned_word.repetitions,
            learned_word.interval,
            learned_word.ease_factor,
            learned_word.mastered,
        )

        return learned_word
