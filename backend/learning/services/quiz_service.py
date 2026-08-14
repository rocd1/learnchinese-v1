from __future__ import annotations

import logging
import unicodedata

from django.db import transaction
from django.utils import timezone

from learning.models import (
    QuizAnswer,
    QuizResult,
    Vocabulary,
)

logger = logging.getLogger("learning.quiz")


class QuizService:
    """
    Business logic for vocabulary quizzes.

    Phase 1 quiz types:

    • Flashcard
    • Matching
    • Typing
    • Word Tile

    Typing modes:

    • Meaning → Chinese
    • Chinese → Pinyin

    Responsibilities:

    • Start quizzes.
    • Select vocabulary questions.
    • Validate quiz types.
    • Validate typing modes.
    • Check user answers.
    • Record quiz answers.
    • Complete quizzes.
    • Calculate quiz scores.
    """

    # ========================================================
    # CONFIGURATION
    # ========================================================

    MIN_QUESTIONS = 1

    MAX_QUESTIONS = 50

    SUPPORTED_QUIZ_TYPES = {
        QuizResult.QuizType.FLASHCARD,
        QuizResult.QuizType.MATCHING,
        QuizResult.QuizType.TYPING,
        QuizResult.QuizType.WORD_TILE,
    }

    TYPING_MODES = {
        QuizResult.TypingMode.MEANING_TO_CHINESE,
        QuizResult.TypingMode.CHINESE_TO_PINYIN,
    }

    # ========================================================
    # START QUIZ
    # ========================================================

    @staticmethod
    @transaction.atomic
    def start_quiz(
        user,
        quiz_type: str,
        hsk_level,
        total_questions: int,
        typing_mode: str = "",
    ) -> tuple[QuizResult, list[Vocabulary]]:
        """
        Create a new quiz and select its vocabulary questions.

        Returns:

            (
                QuizResult,
                list[Vocabulary],
            )
        """

        QuizService.validate_quiz_type(
            quiz_type=quiz_type,
        )

        QuizService.validate_question_count(
            total_questions=total_questions,
        )

        QuizService.validate_typing_mode(
            quiz_type=quiz_type,
            typing_mode=typing_mode,
        )

        vocabulary = list(
            Vocabulary.objects
            .filter(
                hsk_level=hsk_level,
            )
            .order_by("hsk_id", "id")[:total_questions]
        )

        if len(vocabulary) < total_questions:
            raise ValueError(
                "Not enough vocabulary available "
                "for this HSK level."
            )

        quiz = QuizResult.objects.create(
            user=user,
            quiz_type=quiz_type,
            hsk_level=hsk_level,
            total_questions=total_questions,
            correct_answers=0,
            raw_score=0,
            duration_seconds=0,
            typing_mode=typing_mode,
        )

        logger.info(
            "Quiz started: user=%s quiz=%s type=%s "
            "hsk_level=%s questions=%s",
            user.pk,
            quiz.pk,
            quiz_type,
            hsk_level.pk,
            total_questions,
        )

        return quiz, vocabulary

    # ========================================================
    # VALIDATE QUIZ TYPE
    # ========================================================

    @staticmethod
    def validate_quiz_type(
        quiz_type: str,
    ) -> None:
        """
        Ensure the quiz type is implemented in Phase 1.
        """

        if quiz_type not in QuizService.SUPPORTED_QUIZ_TYPES:
            raise ValueError(
                f"Quiz type '{quiz_type}' "
                "is not currently supported."
            )

    # ========================================================
    # VALIDATE QUESTION COUNT
    # ========================================================

    @staticmethod
    def validate_question_count(
        total_questions: int,
    ) -> None:
        """
        Ensure the requested question count is valid.
        """

        if not (
            QuizService.MIN_QUESTIONS
            <= total_questions
            <= QuizService.MAX_QUESTIONS
        ):
            raise ValueError(
                "Question count must be between "
                f"{QuizService.MIN_QUESTIONS} and "
                f"{QuizService.MAX_QUESTIONS}."
            )

    # ========================================================
    # VALIDATE TYPING MODE
    # ========================================================

    @staticmethod
    def validate_typing_mode(
        quiz_type: str,
        typing_mode: str = "",
    ) -> None:
        """
        Ensure typing_mode is used only by typing quizzes.
        """

        if quiz_type == QuizResult.QuizType.TYPING:

            if typing_mode not in QuizService.TYPING_MODES:
                raise ValueError(
                    "A valid typing mode is required "
                    "for typing quizzes."
                )

            return

        if typing_mode:
            raise ValueError(
                "typing_mode can only be used "
                "with typing quizzes."
            )

    # ========================================================
    # GET EXPECTED ANSWER
    # ========================================================

    @staticmethod
    def get_expected_answer(
        vocabulary: Vocabulary,
        quiz_type: str,
        typing_mode: str = "",
    ) -> str:
        """
        Determine the correct answer for a question.
        """

        # ----------------------------------------------------
        # TYPING
        # ----------------------------------------------------

        if quiz_type == QuizResult.QuizType.TYPING:

            if (
                typing_mode
                == QuizResult.TypingMode.MEANING_TO_CHINESE
            ):
                return vocabulary.simplified.strip()

            if (
                typing_mode
                == QuizResult.TypingMode.CHINESE_TO_PINYIN
            ):
                return vocabulary.pinyin.strip()

            raise ValueError(
                "Invalid typing mode."
            )

        # ----------------------------------------------------
        # FLASHCARD
        # ----------------------------------------------------

        if quiz_type == QuizResult.QuizType.FLASHCARD:
            return vocabulary.simplified.strip()

        # ----------------------------------------------------
        # MATCHING
        # ----------------------------------------------------

        if quiz_type == QuizResult.QuizType.MATCHING:

            if not vocabulary.meaning:
                raise ValueError(
                    "Vocabulary has no meaning."
                )

            return vocabulary.meaning[0]

        # ----------------------------------------------------
        # WORD TILE
        # ----------------------------------------------------

        if quiz_type == QuizResult.QuizType.WORD_TILE:
            return vocabulary.simplified.strip()

        raise ValueError(
            f"Unsupported quiz type: {quiz_type}"
        )

    # ========================================================
    # NORMALIZE ANSWER
    # ========================================================

    @staticmethod
    def normalize_answer(
        answer: str,
    ) -> str:
        """
        Normalize user input before comparison.

        Handles:

        • leading/trailing whitespace
        • Unicode normalization
        • repeated whitespace
        • case differences
        """

        answer = unicodedata.normalize(
            "NFKC",
            answer,
        )

        answer = " ".join(
            answer.strip().split()
        )

        return answer.casefold()

    # ========================================================
    # CHECK ANSWER
    # ========================================================

    @staticmethod
    def check_answer(
        user_answer: str,
        correct_answer: str,
    ) -> bool:
        """
        Compare a user's answer with the expected answer.
        """

        return (
            QuizService.normalize_answer(
                user_answer,
            )
            == QuizService.normalize_answer(
                correct_answer,
            )
        )

    # ========================================================
    # SUBMIT ANSWER
    # ========================================================

    @staticmethod
    @transaction.atomic
    def submit_answer(
        user,
        quiz: QuizResult,
        vocabulary: Vocabulary,
        user_answer: str,
    ) -> QuizAnswer:
        """
        Check and record a user's answer.
        """

        # ----------------------------------------------------
        # Security
        # ----------------------------------------------------

        if quiz.user_id != user.pk:
            raise PermissionError(
                "You do not have access to this quiz."
            )

        if quiz.completed_at is not None:
            raise ValueError(
                "This quiz has already been completed."
            )

        # ----------------------------------------------------
        # Determine expected answer
        # ----------------------------------------------------

        correct_answer = (
            QuizService.get_expected_answer(
                vocabulary=vocabulary,
                quiz_type=quiz.quiz_type,
                typing_mode=quiz.typing_mode,
            )
        )

        is_correct = QuizService.check_answer(
            user_answer=user_answer,
            correct_answer=correct_answer,
        )

        # ----------------------------------------------------
        # Prevent duplicate answers
        # ----------------------------------------------------

        existing_answer = quiz.answers.filter(
            vocabulary=vocabulary,
        ).first()

        if existing_answer:
            raise ValueError(
                "This vocabulary question "
                "has already been answered."
            )

        # ----------------------------------------------------
        # Save answer
        # ----------------------------------------------------

        answer = QuizAnswer.objects.create(
            quiz=quiz,
            vocabulary=vocabulary,
            user_answer=user_answer.strip(),
            correct_answer=correct_answer,
            is_correct=is_correct,
        )

        logger.info(
            "Quiz answer recorded: user=%s quiz=%s "
            "vocabulary=%s correct=%s",
            user.pk,
            quiz.pk,
            vocabulary.pk,
            is_correct,
        )

        return answer

    # ========================================================
    # COMPLETE QUIZ
    # ========================================================

    @staticmethod
    @transaction.atomic
    def complete_quiz(
        user,
        quiz: QuizResult,
        duration_seconds: int,
    ) -> QuizResult:
        """
        Complete a quiz and calculate its final score.
        """

        # ----------------------------------------------------
        # Security
        # ----------------------------------------------------

        if quiz.user_id != user.pk:
            raise PermissionError(
                "You do not have access to this quiz."
            )

        if quiz.completed_at is not None:
            raise ValueError(
                "This quiz has already been completed."
            )

        if duration_seconds < 0:
            raise ValueError(
                "Duration cannot be negative."
            )

        # ----------------------------------------------------
        # Calculate score
        # ----------------------------------------------------

        answers = quiz.answers.all()

        correct_answers = answers.filter(
            is_correct=True,
        ).count()

        answered_questions = answers.count()

        raw_score = 0

        if quiz.total_questions > 0:
            raw_score = round(
                (
                    correct_answers
                    / quiz.total_questions
                )
                * 100
            )

        # ----------------------------------------------------
        # Update quiz
        # ----------------------------------------------------

        quiz.correct_answers = correct_answers

        quiz.raw_score = raw_score

        quiz.duration_seconds = duration_seconds

        quiz.completed_at = timezone.now()

        quiz.save(
            update_fields=[
                "correct_answers",
                "raw_score",
                "duration_seconds",
                "completed_at",
            ],
        )

        logger.info(
            "Quiz completed: user=%s quiz=%s "
            "answered=%s correct=%s score=%s",
            user.pk,
            quiz.pk,
            answered_questions,
            correct_answers,
            raw_score,
        )

        return quiz