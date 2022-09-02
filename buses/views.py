from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from buses.models import Bus
from buses.serializers import BusAllocationSerializer, BusSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()


class BusListView(ListModelMixin, GenericAPIView):

    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BusAllocateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            serializer = BusAllocationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = User.objects.get(pk=request.user.id)
            requested_bus = serializer.validated_data["bus"]

            user.bus = requested_bus
            user.save()
        except Exception as e:
            print(e)
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"status": True}, status=status.HTTP_202_ACCEPTED)
