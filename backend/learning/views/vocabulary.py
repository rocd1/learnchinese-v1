from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from learning.models import Vocabulary
from learning.serializers import (
    VocabularyListSerializer,
    VocabularyDetailSerializer,
)


class VocabularyListView(generics.ListAPIView):

    queryset = (
        Vocabulary.objects
        .select_related("hsk_level")
        .order_by(
            "hsk_level__level",
            "hsk_id",
        )
    )

    serializer_class = VocabularyListSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = [
        "simplified",
        "traditional",
        "pinyin",
        "meaning_text",
    ]

    ordering_fields = [
        "hsk_id",
        "simplified",
    ]


class VocabularyDetailView(generics.RetrieveAPIView):

    queryset = (
        Vocabulary.objects
        .select_related("hsk_level")
        .prefetch_related(
            "examples",
            "lessons",
        )
    )

    serializer_class = VocabularyDetailSerializer