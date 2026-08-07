from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from learning.models import QuizResult
from learning.serializers import QuizResultSerializer


class QuizResultListView(generics.ListAPIView):

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = QuizResultSerializer

    def get_queryset(self):

        return (
            QuizResult.objects
            .filter(
                user=self.request.user,
            )
            .prefetch_related("answers")
            .order_by("-completed_at")
        )


class QuizResultDetailView(generics.RetrieveAPIView):

    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = QuizResultSerializer

    def get_queryset(self):

        return (
            QuizResult.objects
            .filter(
                user=self.request.user,
            )
            .prefetch_related("answers")
        )