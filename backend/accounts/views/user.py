from django.contrib.auth import logout

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.user import (
    UserProfileSerializer,
    UserUpdateSerializer,
    AvatarSerializer,
    DeleteAccountSerializer,
)


from accounts.utils.jwt import (
    blacklist_refresh_token,
)

from accounts.utils.cookies import (
    clear_jwt_cookies,
    get_refresh_token,
)


# ============================================================
# UPDATE PROFILE
# ============================================================

class UpdateProfileView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request):

        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            UserProfileSerializer(
                request.user
            ).data,
            status=status.HTTP_200_OK,
        )



# ============================================================
# UPDATE AVATAR
# ============================================================
'''
class UpdateAvatarView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request):

        serializer = AvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            UserProfileSerializer(
                request.user
            ).data,
            status=status.HTTP_200_OK,
        )
'''

class UpdateAvatarView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request):


        serializer = AvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            UserProfileSerializer(
                request.user
            ).data,
            status=status.HTTP_200_OK,
        )



# ============================================================
# DELETE ACCOUNT
# ============================================================

class DeleteAccountView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self, request):

        serializer = DeleteAccountSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        refresh_token = get_refresh_token(
            request,
        )

        blacklist_refresh_token(
            refresh_token,
        )

        user = request.user

        logout(request)


        response = Response(
            {
                "message":
                    "Account deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )

        clear_jwt_cookies(
            response,
        )

        user.delete()

        return response


