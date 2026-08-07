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