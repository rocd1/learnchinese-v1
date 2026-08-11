from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from learning.models import (
    LearnedWord,
    FavoriteWord,
)

from learning.serializers import (
    LearnedWordSerializer,
    FavoriteWordSerializer,
)


class LearnedWordListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = LearnedWordSerializer

    def get_queryset(self):

        return (
            LearnedWord.objects
            .filter(
                user=self.request.user,
            )
            .select_related(
                "vocabulary",
                "vocabulary__hsk_level",
            )
        )


class FavoriteWordListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = FavoriteWordSerializer

    def get_queryset(self):

        return (
            FavoriteWord.objects
            .filter(
                user=self.request.user,
            )
            .select_related(
                "vocabulary",
                "vocabulary__hsk_level",
            )
        )






from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.serializers.learning import (
    LearnedWordSerializer,
    LearningSessionAnswerSerializer,
)
from learning.serializers.vocabulary import VocabularyListSerializer
from learning.services.learning_service import LearningService


# ============================================================
# LEARNING SESSION
# ============================================================


class LearningSessionView(APIView):
    """
    Return vocabulary for the user's learning session.

    GET /api/learning/session/
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Return vocabulary that the user should study.
        """

        limit = request.query_params.get(
            "limit",
            LearningService.DEFAULT_SESSION_SIZE,
        )

        try:
            limit = int(limit)

        except (TypeError, ValueError):

            return Response(
                {
                    "detail": "limit must be an integer.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            limit < LearningService.MIN_SESSION_SIZE
            or limit > LearningService.MAX_SESSION_SIZE
        ):

            return Response(
                {
                    "detail": (
                        f"limit must be between "
                        f"{LearningService.MIN_SESSION_SIZE} "
                        f"and "
                        f"{LearningService.MAX_SESSION_SIZE}."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        vocabulary = LearningService.get_session(
            user=request.user,
            limit=limit,
        )

        serializer = VocabularyListSerializer(
            vocabulary,
            many=True,
        )

        return Response(
            {
                "count": len(vocabulary),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# LEARNING SESSION ANSWER
# ============================================================


class LearningSessionAnswerView(APIView):
    """
    Record the user's answer for a vocabulary word.

    POST /api/learning/session/answer/
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        """
        Record whether the user's answer was correct.
        """

        serializer = LearningSessionAnswerSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        vocabulary = serializer.validated_data[
            "vocabulary"
        ]

        correct = serializer.validated_data[
            "correct"
        ]

        learned_word = LearningService.record_answer(
            user=request.user,
            vocabulary=vocabulary,
            correct=correct,
        )

        response_serializer = LearnedWordSerializer(
            learned_word,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )