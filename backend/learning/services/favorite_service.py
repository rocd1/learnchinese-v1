from learning.models import FavoriteWord


class FavoriteService:
    """
    Business logic for managing user favorites.
    """

    # =========================================================
    # GET USER FAVORITES
    # =========================================================

    @staticmethod
    def get_user_favorites(user):
        """
        Return all favorites belonging to the authenticated user.
        """

        return (
            FavoriteWord.objects
            .filter(user=user)
            .select_related("vocabulary")
        )

    # =========================================================
    # TOGGLE FAVORITE
    # =========================================================

    @staticmethod
    def toggle(user, vocabulary):
        """
        Add the vocabulary to favorites if it is not currently
        favorited.

        Remove it if it is already favorited.
        """

        favorite = FavoriteWord.objects.filter(
            user=user,
            vocabulary=vocabulary,
        ).first()

        if favorite:
            favorite.delete()

            return {
                "is_favorite": False,
                "favorite_id": None,
            }

        favorite = FavoriteWord.objects.create(
            user=user,
            vocabulary=vocabulary,
        )

        return {
            "is_favorite": True,
            "favorite_id": favorite.id,
        }

    # =========================================================
    # CHECK FAVORITE
    # =========================================================

    @staticmethod
    def exists(user, vocabulary):
        """
        Check whether a vocabulary word is favorited by the user.
        """

        return FavoriteWord.objects.filter(
            user=user,
            vocabulary=vocabulary,
        ).exists()
