from __future__ import annotations

import unicodedata

from django.utils import timezone

from learning.models import QuizResult, Vocabulary


class GuestQuizService:
    """
    Business logic for guest vocabulary practice quizzes.

    Guest quizzes are temporary and are NOT stored as QuizResult records.

    Quiz state is stored in Django's signed session.

    Phase 1 quiz types:

    • Flashcard
    • Matching
    • Typing
    • Word Tile

    Typing modes:

    • Meaning → Chinese
    • Chinese → Pinyin
    """

    # ========================================================
    # CONFIGURATION
    # ========================================================

    SESSION_KEY = "guest_quiz"

    MIN_QUESTIONS = 1
    MAX_QUESTIONS = 10

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
    # VALIDATION
    # ========================================================

    @classmethod
    def validate_quiz_type(
        cls,
        quiz_type: str,
    ) -> None:
        """
        Ensure the requested quiz type is supported.
        """

        if quiz_type not in cls.SUPPORTED_QUIZ_TYPES:
            raise ValueError(
                f"Quiz type '{quiz_type}' "
                "is not currently supported."
            )

    @classmethod
    def validate_question_count(
        cls,
        total_questions: int,
    ) -> None:
        """
        Validate the number of guest questions.
        """

        if not (
            cls.MIN_QUESTIONS
            <= total_questions
            <= cls.MAX_QUESTIONS
        ):
            raise ValueError(
                "Question count must be between "
                f"{cls.MIN_QUESTIONS} and "
                f"{cls.MAX_QUESTIONS}."
            )

    @classmethod
    def validate_typing_mode(
        cls,
        quiz_type: str,
        typing_mode: str = "",
    ) -> None:
        """
        Validate typing mode usage.
        """

        if quiz_type == QuizResult.QuizType.TYPING:

            if typing_mode not in cls.TYPING_MODES:
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
    # START GUEST QUIZ
    # ========================================================

    @classmethod
    def start_quiz(
        cls,
        request,
        quiz_type: str,
        hsk_level,
        total_questions: int,
        typing_mode: str = "",
    ) -> dict:
        """
        Start a guest quiz.

        No QuizResult is created.

        Quiz state is stored in the Django session.

        Returns quiz information and the selected questions.
        """

        cls.validate_quiz_type(
            quiz_type=quiz_type,
        )

        cls.validate_question_count(
            total_questions=total_questions,
        )

        cls.validate_typing_mode(
            quiz_type=quiz_type,
            typing_mode=typing_mode,
        )

        # ----------------------------------------------------
        # Prevent starting another quiz while one is active
        # ----------------------------------------------------

        if cls.SESSION_KEY in request.session:
            print(
                "[GUEST QUIZ DEBUG] "
                "Quiz already exists in session."
            )

            print(
                "[GUEST QUIZ DEBUG] Session key:",
                request.session.session_key,
            )

            print(
                "[GUEST QUIZ DEBUG] Existing session data:",
                request.session.get(cls.SESSION_KEY),
            )

            raise ValueError(
                "A guest quiz is already in progress."
            )

        # ----------------------------------------------------
        # Select vocabulary
        # ----------------------------------------------------

        vocabulary = list(
            Vocabulary.objects
            .filter(
                hsk_level=hsk_level,
            )
            .order_by(
                "hsk_id",
                "id",
            )[:total_questions]
        )

        if len(vocabulary) < total_questions:
            raise ValueError(
                "Not enough vocabulary available "
                "for this HSK level."
            )

        vocabulary_ids = [
            vocabulary_item.pk
            for vocabulary_item in vocabulary
        ]

        # ----------------------------------------------------
        # Store quiz state in session
        # ----------------------------------------------------

        request.session[cls.SESSION_KEY] = {
            "quiz_type": quiz_type,
            "typing_mode": typing_mode,
            "hsk_level_id": hsk_level.pk,
            "total_questions": total_questions,
            "vocabulary_ids": vocabulary_ids,
            "answers": [],
            "correct_answers": 0,
            "started_at": timezone.now().isoformat(),
        }

        request.session.modified = True

        # ----------------------------------------------------
        # DEBUG: verify session after storing quiz
        # ----------------------------------------------------

        print(
            "\n=================================================="
        )
        print(
            "[GUEST QUIZ DEBUG] START QUIZ"
        )
        print(
            "=================================================="
        )

        print(
            "[GUEST QUIZ DEBUG] Session key:",
            request.session.session_key,
        )

        print(
            "[GUEST QUIZ DEBUG] Session data:",
            request.session.get(cls.SESSION_KEY),
        )

        print(
            "[GUEST QUIZ DEBUG] Vocabulary IDs:",
            vocabulary_ids,
        )

        print(
            "==================================================\n"
        )

        # ----------------------------------------------------
        # Build response
        # ----------------------------------------------------

        questions = []

        for item in vocabulary:
            question = {
                "id": item.pk,
            }

            if quiz_type == QuizResult.QuizType.FLASHCARD:
                question.update(
                    {
                        "simplified": item.simplified,
                        "pinyin": item.pinyin,
                        "meaning": item.meaning,
                    }
                )

            elif quiz_type == QuizResult.QuizType.MATCHING:
                question.update(
                    {
                        "simplified": item.simplified,
                        "meaning": item.meaning,
                    }
                )

            elif quiz_type == QuizResult.QuizType.TYPING:

                if (
                    typing_mode
                    == QuizResult.TypingMode.MEANING_TO_CHINESE
                ):
                    question["meaning"] = item.meaning

                elif (
                    typing_mode
                    == QuizResult.TypingMode.CHINESE_TO_PINYIN
                ):
                    question["simplified"] = item.simplified

            elif quiz_type == QuizResult.QuizType.WORD_TILE:
                question["simplified"] = item.simplified

            questions.append(question)

        return {
            "quiz_type": quiz_type,
            "typing_mode": typing_mode,
            "hsk_level": hsk_level.pk,
            "total_questions": total_questions,
            "questions": questions,
        }

    # ========================================================
    # GET CURRENT QUIZ
    # ========================================================

    @classmethod
    def get_current_quiz(
        cls,
        request,
    ) -> dict:
        """
        Return the active guest quiz stored in the session.

        Raises ValueError when no guest quiz is active.
        """

        quiz = request.session.get(
            cls.SESSION_KEY,
        )

        # ----------------------------------------------------
        # DEBUG: inspect session received by request
        # ----------------------------------------------------

        print(
            "\n=================================================="
        )
        print(
            "[GUEST QUIZ DEBUG] GET CURRENT QUIZ"
        )
        print(
            "=================================================="
        )

        print(
            "[GUEST QUIZ DEBUG] Session key:",
            request.session.session_key,
        )

        print(
            "[GUEST QUIZ DEBUG] Session data:",
            quiz,
        )

        print(
            "==================================================\n"
        )

        if not quiz:
            raise ValueError(
                "No guest quiz is currently in progress."
            )

        return quiz

    # ========================================================
    # EXPECTED ANSWER
    # ========================================================

    @classmethod
    def get_expected_answer(
        cls,
        vocabulary: Vocabulary,
        quiz_type: str,
        typing_mode: str = "",
    ) -> str:
        """
        Determine the expected answer for a guest question.
        """

        cls.validate_quiz_type(
            quiz_type=quiz_type,
        )

        cls.validate_typing_mode(
            quiz_type=quiz_type,
            typing_mode=typing_mode,
        )

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

            return str(
                vocabulary.meaning[0]
            ).strip()

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
        Normalize guest input before comparison.
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

    @classmethod
    def check_answer(
        cls,
        user_answer: str,
        correct_answer: str,
    ) -> bool:
        """
        Compare a guest answer with the expected answer.
        """

        return (
            cls.normalize_answer(user_answer)
            == cls.normalize_answer(correct_answer)
        )

    # ========================================================
    # SUBMIT ANSWER
    # ========================================================

    @classmethod
    def submit_answer(
        cls,
        request,
        vocabulary_id: int,
        user_answer: str,
    ) -> dict:
        """
        Check and record a guest answer.

        Guest answers are stored temporarily in the session.
        """

        quiz = cls.get_current_quiz(
            request,
        )

        # ----------------------------------------------------
        # Prevent answering after all questions are answered
        # ----------------------------------------------------

        answers = quiz.get(
            "answers",
            [],
        )

        if len(answers) >= quiz["total_questions"]:
            raise ValueError(
                "All quiz questions have already been answered."
            )

        # ----------------------------------------------------
        # Ensure vocabulary belongs to this quiz
        # ----------------------------------------------------

        vocabulary_ids = quiz.get(
            "vocabulary_ids",
            [],
        )

        print(
            "\n=================================================="
        )
        print(
            "[GUEST QUIZ DEBUG] SUBMIT ANSWER"
        )
        print(
            "=================================================="
        )

        print(
            "[GUEST QUIZ DEBUG] Session key:",
            request.session.session_key,
        )

        print(
            "[GUEST QUIZ DEBUG] Request vocabulary ID:",
            vocabulary_id,
        )

        print(
            "[GUEST QUIZ DEBUG] Session vocabulary IDs:",
            vocabulary_ids,
        )

        print(
            "[GUEST QUIZ DEBUG] Vocabulary ID type:",
            type(vocabulary_id),
        )

        print(
            "[GUEST QUIZ DEBUG] Session vocabulary ID types:",
            [type(item) for item in vocabulary_ids],
        )

        print(
            "[GUEST QUIZ DEBUG] Membership check:",
            vocabulary_id in vocabulary_ids,
        )

        print(
            "==================================================\n"
        )

        if vocabulary_id not in vocabulary_ids:
            raise ValueError(
                "This vocabulary question does not belong "
                "to the current guest quiz."
            )

        # ----------------------------------------------------
        # Prevent duplicate answers
        # ----------------------------------------------------

        for answer in answers:
            if answer["vocabulary_id"] == vocabulary_id:
                raise ValueError(
                    "This vocabulary question "
                    "has already been answered."
                )

        # ----------------------------------------------------
        # Get vocabulary
        # ----------------------------------------------------

        try:
            vocabulary = Vocabulary.objects.get(
                pk=vocabulary_id,
            )
        except Vocabulary.DoesNotExist:
            raise ValueError(
                "Vocabulary not found."
            )

        # ----------------------------------------------------
        # Determine correct answer
        # ----------------------------------------------------

        correct_answer = cls.get_expected_answer(
            vocabulary=vocabulary,
            quiz_type=quiz["quiz_type"],
            typing_mode=quiz.get(
                "typing_mode",
                "",
            ),
        )

        # ----------------------------------------------------
        # Check answer
        # ----------------------------------------------------

        is_correct = cls.check_answer(
            user_answer=user_answer,
            correct_answer=correct_answer,
        )

        # ----------------------------------------------------
        # Record answer
        # ----------------------------------------------------

        answer_data = {
            "vocabulary_id": vocabulary_id,
            "user_answer": user_answer.strip(),
            "correct_answer": correct_answer,
            "is_correct": is_correct,
        }

        answers.append(
            answer_data,
        )

        quiz["answers"] = answers

        if is_correct:
            quiz["correct_answers"] = (
                quiz.get(
                    "correct_answers",
                    0,
                )
                + 1
            )

        request.session[cls.SESSION_KEY] = quiz
        request.session.modified = True

        # ----------------------------------------------------
        # DEBUG: verify session after answer
        # ----------------------------------------------------

        print(
            "[GUEST QUIZ DEBUG] Answer recorded."
        )

        print(
            "[GUEST QUIZ DEBUG] Updated session:",
            request.session.get(cls.SESSION_KEY),
        )

        # ----------------------------------------------------
        # Return result
        # ----------------------------------------------------

        return {
            "vocabulary": {
                "id": vocabulary.pk,
                "simplified": vocabulary.simplified,
                "pinyin": vocabulary.pinyin,
                "meaning": vocabulary.meaning,
            },
            "user_answer": user_answer.strip(),
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "answered_questions": len(answers),
            "total_questions": quiz["total_questions"],
        }

    # ========================================================
    # COMPLETE QUIZ
    # ========================================================

    @classmethod
    def complete_quiz(
        cls,
        request,
    ) -> dict:
        """
        Complete the current guest quiz.

        No QuizResult is created.
        """

        quiz = cls.get_current_quiz(
            request,
        )

        answers = quiz.get(
            "answers",
            [],
        )

        answered_questions = len(
            answers,
        )

        correct_answers = sum(
            1
            for answer in answers
            if answer["is_correct"]
        )

        total_questions = quiz[
            "total_questions"
        ]

        raw_score = 0

        if total_questions > 0:
            raw_score = round(
                (
                    correct_answers
                    / total_questions
                )
                * 100
            )

        # ----------------------------------------------------
        # Calculate duration
        # ----------------------------------------------------

        duration_seconds = 0

        started_at = quiz.get(
            "started_at",
        )

        if started_at:
            try:
                started = timezone.datetime.fromisoformat(
                    started_at,
                )

                if timezone.is_naive(started):
                    started = timezone.make_aware(
                        started,
                    )

                duration_seconds = max(
                    0,
                    int(
                        (
                            timezone.now()
                            - started
                        ).total_seconds()
                    ),
                )

            except (TypeError, ValueError):
                duration_seconds = 0

        result = {
            "quiz_type": quiz["quiz_type"],
            "typing_mode": quiz.get(
                "typing_mode",
                "",
            ),
            "hsk_level": quiz[
                "hsk_level_id"
            ],
            "total_questions": total_questions,
            "answered_questions": answered_questions,
            "correct_answers": correct_answers,
            "raw_score": raw_score,
            "duration_seconds": duration_seconds,
            "answers": answers,
        }

        # ----------------------------------------------------
        # Remove guest quiz from session
        # ----------------------------------------------------

        request.session.pop(
            cls.SESSION_KEY,
            None,
        )

        request.session.modified = True

        return result

    # ========================================================
    # ABANDON QUIZ
    # ========================================================

    @classmethod
    def abandon_quiz(
        cls,
        request,
    ) -> dict:
        """
        Abandon the current guest quiz.

        The temporary quiz state is removed from the session.
        """

        quiz = cls.get_current_quiz(
            request,
        )

        answered_questions = len(
            quiz.get(
                "answers",
                [],
            )
        )

        result = {
            "quiz_type": quiz["quiz_type"],
            "typing_mode": quiz.get(
                "typing_mode",
                "",
            ),
            "hsk_level": quiz[
                "hsk_level_id"
            ],
            "total_questions": quiz[
                "total_questions"
            ],
            "answered_questions": answered_questions,
            "status": "abandoned",
        }

        # ----------------------------------------------------
        # Remove quiz from session
        # ----------------------------------------------------

        request.session.pop(
            cls.SESSION_KEY,
            None,
        )

        request.session.modified = True

        print(
            "[GUEST QUIZ DEBUG] Quiz abandoned."
        )

        print(
            "[GUEST QUIZ DEBUG] Session key:",
            request.session.session_key,
        )

        print(
            "[GUEST QUIZ DEBUG] Session after abandon:",
            request.session.get(cls.SESSION_KEY),
        )

        return result
