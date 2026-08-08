from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.serializers.favorite import (
    FavoriteSerializer,
    FavoriteToggleSerializer,
)
from learning.services.favorite_service import FavoriteService


# ============================================================
# FAVORITE LIST
# ============================================================

class FavoriteListView(APIView):
    """
    Return the authenticated user's favorite vocabulary words.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Return all favorites belonging to the current user.
        """

        favorites = FavoriteService.get_user_favorites(
            request.user,
        )

        serializer = FavoriteSerializer(
            favorites,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# FAVORITE TOGGLE
# ============================================================

class FavoriteToggleView(APIView):
    """
    Toggle a vocabulary word as a favorite.

    If the word is not currently favorited:
        → Create a FavoriteWord.

    If the word is already favorited:
        → Remove the FavoriteWord.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        """
        Add or remove a vocabulary word from favorites.
        """

        serializer = FavoriteToggleSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        vocabulary = serializer.validated_data["vocabulary"]

        result = FavoriteService.toggle(
            user=request.user,
            vocabulary=vocabulary,
        )

        return Response(
            {
                "vocabulary": vocabulary.id,
                **result,
            },
            status=status.HTTP_200_OK,
        )
