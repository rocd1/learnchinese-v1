from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.serializers.dashboard import (
    DashboardStatisticsSerializer,
)
from learning.services.dashboard_service import (
    DashboardService,
)


class DashboardStatisticsView(APIView):
    """
    Return statistics for the authenticated user's dashboard.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        Return dashboard statistics.
        """

        statistics = DashboardService.get_statistics(
            user=request.user,
        )

        serializer = DashboardStatisticsSerializer(
            statistics,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )