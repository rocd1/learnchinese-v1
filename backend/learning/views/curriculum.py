from rest_framework import generics

from learning.models import (
    HSKLevel,
)

from learning.serializers import (
    HSKLevelListSerializer,
    HSKLevelDetailSerializer,
)


class HSKLevelListView(generics.ListAPIView):

    queryset = (
        HSKLevel.objects
        .filter(active=True)
        .order_by("level")
    )

    serializer_class = HSKLevelListSerializer


class HSKLevelDetailView(generics.RetrieveAPIView):

    queryset = (
        HSKLevel.objects
        .prefetch_related("lessons")
    )

    serializer_class = HSKLevelDetailSerializer