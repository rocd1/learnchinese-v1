from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import QuizResult
from learning.serializers.quiz import (
    QuizAnswerSubmitSerializer,
    QuizCompleteSerializer,
    QuizResultSerializer,
    QuizStartSerializer,
    QuizAnswerSerializer,
)
from learning.services.quiz_service import QuizService

from django.shortcuts import get_object_or_404

from learning.models import (
    QuizResult,
)

from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
    ValidationError,
)

from learning.models import QuizResult



# ============================================================
# START QUIZ
# ============================================================


class QuizStartView(APIView):
    """
    Start a new quiz for the authenticated user.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = QuizStartSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        quiz = QuizService.start_quiz(
            user=request.user,
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

        response_serializer = QuizResultSerializer(
            quiz,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


# ============================================================
# SUBMIT ANSWER
# ============================================================

class QuizAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = QuizAnswerSubmitSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        try:
            quiz = QuizResult.objects.get(
                pk=pk,
                user=request.user,
            )
        except QuizResult.DoesNotExist:
            raise NotFound("Quiz not found.")

        try:
            answer = QuizService.submit_answer(
                user=request.user,
                quiz=quiz,
                vocabulary=serializer.validated_data["vocabulary"],
                user_answer=serializer.validated_data["user_answer"],
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc))
        except ValueError as exc:
            raise ValidationError(str(exc))

        return Response(
            QuizAnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED,
        )






# ============================================================
# COMPLETE QUIZ
# ============================================================


class QuizCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = QuizCompleteSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        try:
            quiz = QuizResult.objects.get(
                pk=pk,
                user=request.user,
            )
        except QuizResult.DoesNotExist:
            raise NotFound("Quiz not found.")

        try:
            quiz = QuizService.complete_quiz(
                user=request.user,
                quiz=quiz,
                duration_seconds=serializer.validated_data[
                    "duration_seconds"
                ],
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc))
        except ValueError as exc:
            raise ValidationError(str(exc))

        return Response(
            QuizResultSerializer(quiz).data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# QUIZ HISTORY
# ============================================================


class QuizResultListView(APIView):
    """
    Return the authenticated user's quiz history.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        quizzes = QuizResult.objects.filter(
            user=request.user,
        ).select_related(
            "hsk_level",
        )

        serializer = QuizResultSerializer(
            quizzes,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )