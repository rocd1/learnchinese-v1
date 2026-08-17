from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.serializers.guest_quiz import (
    GuestQuizAnswerSerializer,
    GuestQuizStartSerializer,
)

from learning.services.guest_quiz_service import GuestQuizService


# ============================================================
# START GUEST QUIZ
# ============================================================


class GuestQuizStartView(APIView):
    """
    Start a new guest practice quiz.

    Guest quiz state is stored in Django's signed session.
    No user account is required.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuestQuizStartSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:
            quiz_data = GuestQuizService.start_quiz(
                request=request,
                quiz_type=serializer.validated_data["quiz_type"],
                hsk_level=serializer.validated_data["hsk_level"],
                total_questions=serializer.validated_data[
                    "total_questions"
                ],
                typing_mode=serializer.validated_data.get(
                    "typing_mode",
                    "",
                ),
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            quiz_data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# SUBMIT GUEST ANSWER
# ============================================================


class GuestQuizAnswerView(APIView):
    """
    Submit an answer to the current guest quiz.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GuestQuizAnswerSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:
            result = GuestQuizService.submit_answer(
                request=request,
                vocabulary_id=serializer.validated_data[
                    "vocabulary"
                ].pk,
                user_answer=serializer.validated_data[
                    "user_answer"
                ],
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# COMPLETE GUEST QUIZ
# ============================================================


class GuestQuizCompleteView(APIView):
    """
    Complete the current guest quiz.

    The final result is returned but is not persisted
    as a QuizResult belonging to a user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            result = GuestQuizService.complete_quiz(
                request=request,
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )


# ============================================================
# ABANDON GUEST QUIZ
# ============================================================


class GuestQuizAbandonView(APIView):
    """
    Abandon the current guest quiz.

    The active guest quiz state is removed from
    the signed session.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            result = GuestQuizService.abandon_quiz(
                request=request,
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )