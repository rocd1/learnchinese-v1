from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from learning.models import HSKLevel, Vocabulary


class GuestQuizAPITestCase(APITestCase):
    """
    API tests for the guest quiz endpoints.

    These tests verify the complete HTTP/API flow,
    including Django session persistence between requests.

    Covered quiz types:
    - Flashcard
    - Matching
    - Typing
    - Word Tile

    Covered guest quiz lifecycle:
    - Start
    - Current
    - Answer
    - Complete
    - Abandon
    """

    @classmethod
    def setUpTestData(cls):
        cls.hsk_level = HSKLevel.objects.create(
            name="HSK 4",
            level=4,
            total_words=5,
            description="Test HSK level",
            active=True,
        )

        cls.vocabulary = [
            Vocabulary.objects.create(
                hsk_level=cls.hsk_level,
                hsk_id=524,
                slug="test-ai-qing-524",
                simplified="爱情",
                traditional="愛情",
                pinyin="ài qíng",
                meaning=[
                    "romance",
                    "love (romantic)",
                    "CL:個|个[gè]",
                ],
            ),
            Vocabulary.objects.create(
                hsk_level=cls.hsk_level,
                hsk_id=525,
                slug="test-an-pai-525",
                simplified="安排",
                traditional="安排",
                pinyin="ān pái",
                meaning=[
                    "to arrange",
                    "to plan",
                    "to set up",
                ],
            ),
            Vocabulary.objects.create(
                hsk_level=cls.hsk_level,
                hsk_id=526,
                slug="test-an-quan-526",
                simplified="安全",
                traditional="安全",
                pinyin="ān quán",
                meaning=[
                    "safe",
                    "secure",
                    "safety",
                    "security",
                ],
            ),
            Vocabulary.objects.create(
                hsk_level=cls.hsk_level,
                hsk_id=527,
                slug="test-an-527",
                simplified="暗",
                traditional="暗",
                pinyin="àn",
                meaning=[
                    "dark",
                    "to close",
                ],
            ),
            Vocabulary.objects.create(
                hsk_level=cls.hsk_level,
                hsk_id=528,
                slug="test-an-shi-528",
                simplified="按时",
                traditional="按時",
                pinyin="àn shí",
                meaning=[
                    "on time",
                    "on schedule",
                ],
            ),
        ]

    # ========================================================
    # URL HELPERS
    # ========================================================

    @staticmethod
    def start_url():
        return reverse("guest-quiz-start")

    @staticmethod
    def current_url():
        return reverse("guest-quiz-current")

    @staticmethod
    def answer_url():
        return reverse("guest-quiz-answer")

    @staticmethod
    def complete_url():
        return reverse("guest-quiz-complete")

    @staticmethod
    def abandon_url():
        return reverse("guest-quiz-abandon")

    # ========================================================
    # REQUEST HELPERS
    # ========================================================

    def start_flashcard_quiz(
        self,
        total_questions=5,
    ):
        return self.client.post(
            self.start_url(),
            {
                "quiz_type": "flashcard",
                "hsk_level": self.hsk_level.pk,
                "total_questions": total_questions,
            },
            format="json",
        )

    def start_matching_quiz(
        self,
        total_questions=5,
    ):
        return self.client.post(
            self.start_url(),
            {
                "quiz_type": "matching",
                "hsk_level": self.hsk_level.pk,
                "total_questions": total_questions,
            },
            format="json",
        )

    def start_typing_quiz(
        self,
        typing_mode,
        total_questions=5,
    ):
        return self.client.post(
            self.start_url(),
            {
                "quiz_type": "typing",
                "hsk_level": self.hsk_level.pk,
                "total_questions": total_questions,
                "typing_mode": typing_mode,
            },
            format="json",
        )

    def start_word_tile_quiz(
        self,
        total_questions=5,
    ):
        return self.client.post(
            self.start_url(),
            {
                "quiz_type": "word_tile",
                "hsk_level": self.hsk_level.pk,
                "total_questions": total_questions,
            },
            format="json",
        )

    def submit_answer(
        self,
        vocabulary_id,
        user_answer,
    ):
        return self.client.post(
            self.answer_url(),
            {
                "vocabulary": vocabulary_id,
                "user_answer": user_answer,
            },
            format="json",
        )

    # ========================================================
    # START QUIZ
    # ========================================================

    def test_start_flashcard_quiz(self):
        response = self.start_flashcard_quiz()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "flashcard",
        )

        self.assertEqual(
            data["hsk_level"],
            self.hsk_level.pk,
        )

        self.assertEqual(
            data["total_questions"],
            5,
        )

        self.assertEqual(
            len(data["questions"]),
            5,
        )

        self.assertEqual(
            data["questions"][0]["id"],
            self.vocabulary[0].pk,
        )

    def test_start_matching_quiz(self):
        response = self.start_matching_quiz()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "matching",
        )

        self.assertEqual(
            len(data["questions"]),
            5,
        )

        self.assertIn(
            "simplified",
            data["questions"][0],
        )

        self.assertIn(
            "meaning",
            data["questions"][0],
        )

    def test_start_typing_meaning_to_chinese(self):
        response = self.start_typing_quiz(
            typing_mode="meaning_to_chinese",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "typing",
        )

        self.assertEqual(
            data["typing_mode"],
            "meaning_to_chinese",
        )

        self.assertIn(
            "meaning",
            data["questions"][0],
        )

        self.assertNotIn(
            "simplified",
            data["questions"][0],
        )

    def test_start_typing_chinese_to_pinyin(self):
        response = self.start_typing_quiz(
            typing_mode="chinese_to_pinyin",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "typing",
        )

        self.assertEqual(
            data["typing_mode"],
            "chinese_to_pinyin",
        )

        self.assertIn(
            "simplified",
            data["questions"][0],
        )

        self.assertNotIn(
            "meaning",
            data["questions"][0],
        )

    def test_start_word_tile_quiz(self):
        response = self.start_word_tile_quiz()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "word_tile",
        )

        self.assertIn(
            "simplified",
            data["questions"][0],
        )

    # ========================================================
    # CURRENT QUIZ
    # ========================================================

    def test_current_quiz_requires_active_quiz(self):
        response = self.client.get(
            self.current_url(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_current_quiz_returns_active_quiz(self):
        start_response = self.start_flashcard_quiz()

        self.assertEqual(
            start_response.status_code,
            status.HTTP_201_CREATED,
        )

        response = self.client.get(
            self.current_url(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "flashcard",
        )

        self.assertEqual(
            data["total_questions"],
            5,
        )

        self.assertEqual(
            data["vocabulary_ids"],
            [
                vocabulary.pk
                for vocabulary in self.vocabulary
            ],
        )

    # ========================================================
    # ANSWER
    # ========================================================

    def test_submit_correct_flashcard_answer(self):
        self.start_flashcard_quiz()

        response = self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertTrue(
            data["is_correct"],
        )

        self.assertEqual(
            data["correct_answer"],
            "爱情",
        )

        self.assertEqual(
            data["answered_questions"],
            1,
        )

        self.assertEqual(
            data["total_questions"],
            5,
        )

    def test_submit_incorrect_flashcard_answer(self):
        self.start_flashcard_quiz()

        response = self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="错误答案",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        data = response.json()

        self.assertFalse(
            data["is_correct"],
        )

        self.assertEqual(
            data["correct_answer"],
            "爱情",
        )

    def test_submit_answer_persists_session_state(self):
        self.start_flashcard_quiz()

        self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        response = self.client.get(
            self.current_url(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertEqual(
            len(data["answers"]),
            1,
        )

        self.assertEqual(
            data["answers"][0]["vocabulary_id"],
            self.vocabulary[0].pk,
        )

        self.assertTrue(
            data["answers"][0]["is_correct"],
        )

    def test_submit_answer_for_vocabulary_not_in_quiz(self):
        self.start_flashcard_quiz()

        outside_vocabulary = Vocabulary.objects.create(
            hsk_level=self.hsk_level,
            hsk_id=999,
            slug="test-wai-bu-999",
            simplified="测试",
            traditional="測試",
            pinyin="cè shì",
            meaning=["test"],
        )

        response = self.submit_answer(
            vocabulary_id=outside_vocabulary.pk,
            user_answer="测试",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_submit_duplicate_answer_is_rejected(self):
        self.start_flashcard_quiz()

        first_response = self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cannot_answer_without_active_quiz(self):
        response = self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    def test_complete_quiz_with_all_correct_answers(self):
        self.start_flashcard_quiz()

        for vocabulary in self.vocabulary:
            response = self.submit_answer(
                vocabulary_id=vocabulary.pk,
                user_answer=vocabulary.simplified,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
            )

        response = self.client.post(
            self.complete_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "flashcard",
        )

        self.assertEqual(
            data["total_questions"],
            5,
        )

        self.assertEqual(
            data["answered_questions"],
            5,
        )

        self.assertEqual(
            data["correct_answers"],
            5,
        )

        self.assertEqual(
            data["raw_score"],
            100,
        )

        self.assertEqual(
            len(data["answers"]),
            5,
        )

    def test_complete_quiz_with_mixed_results(self):
        self.start_flashcard_quiz()

        answers = [
            "爱情",
            "wrong",
            "安全",
            "wrong",
            "按时",
        ]

        for vocabulary, answer in zip(
            self.vocabulary,
            answers,
        ):
            response = self.submit_answer(
                vocabulary_id=vocabulary.pk,
                user_answer=answer,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
            )

        response = self.client.post(
            self.complete_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertEqual(
            data["answered_questions"],
            5,
        )

        self.assertEqual(
            data["correct_answers"],
            3,
        )

        self.assertEqual(
            data["raw_score"],
            60,
        )

    def test_complete_quiz_removes_session(self):
        self.start_flashcard_quiz()

        response = self.client.post(
            self.complete_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        current_response = self.client.get(
            self.current_url(),
        )

        self.assertEqual(
            current_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_complete_requires_active_quiz(self):
        response = self.client.post(
            self.complete_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ========================================================
    # ABANDON
    # ========================================================

    def test_abandon_quiz(self):
        self.start_flashcard_quiz()

        self.submit_answer(
            vocabulary_id=self.vocabulary[0].pk,
            user_answer="爱情",
        )

        response = self.client.post(
            self.abandon_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()

        self.assertEqual(
            data["quiz_type"],
            "flashcard",
        )

        self.assertEqual(
            data["total_questions"],
            5,
        )

        self.assertEqual(
            data["answered_questions"],
            1,
        )

        self.assertEqual(
            data["status"],
            "abandoned",
        )

    def test_abandon_quiz_removes_session(self):
        self.start_flashcard_quiz()

        response = self.client.post(
            self.abandon_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        current_response = self.client.get(
            self.current_url(),
        )

        self.assertEqual(
            current_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_abandon_requires_active_quiz(self):
        response = self.client.post(
            self.abandon_url(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ========================================================
    # START VALIDATION
    # ========================================================

    def test_cannot_start_second_quiz_while_one_is_active(self):
        first_response = self.start_flashcard_quiz()

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.start_matching_quiz()

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_quiz_type_is_rejected(self):
        response = self.client.post(
            self.start_url(),
            {
                "quiz_type": "invalid",
                "hsk_level": self.hsk_level.pk,
                "total_questions": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_question_count_is_rejected(self):
        response = self.client.post(
            self.start_url(),
            {
                "quiz_type": "flashcard",
                "hsk_level": self.hsk_level.pk,
                "total_questions": 11,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_typing_quiz_requires_typing_mode(self):
        response = self.client.post(
            self.start_url(),
            {
                "quiz_type": "typing",
                "hsk_level": self.hsk_level.pk,
                "total_questions": 5,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_typing_mode_cannot_be_used_with_flashcard(self):
        response = self.client.post(
            self.start_url(),
            {
                "quiz_type": "flashcard",
                "hsk_level": self.hsk_level.pk,
                "total_questions": 5,
                "typing_mode": "meaning_to_chinese",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
