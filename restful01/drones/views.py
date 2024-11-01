from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from drones.models import DroneCategory, Drone, Pilot, Competition
from drones.serializers import (
    DroneCategorySerializer,
    DroneSerializer,
    PilotSerializer,
    PilotCompetitionSerializer,
)
from drones.filters import CompetitionFilter
from rest_framework import permissions
from drones import custom_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "drones-categories": reverse("dronecategory-list", request=request),
                "drones": reverse(DroneList.name, request=request),
                "pilots": reverse(PilotList.name, request=request),
                "competitions": reverse(CompetitionList.name, request=request),
            }
        )


class DroneCategoryViewSet(viewsets.ModelViewSet):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    search_fields = ("^name",)
    ordering_fields = ("name",)


class DroneList(generics.ListCreateAPIView):
    throttle_scope = "drones"
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-list"
    filterset_fields = (
        "drone_category",
        "has_it_competed",
        "manufacturing_date",
        "has_it_competed",
    )
    # Quando não utilizamos nenhum simbolo na frente do campo a ser pesquisado,
    # vai retornar toda instância de Drone que tenha a ocorrência da palavra
    # ou letra inserida no campo de busca
    # ^ que começa com
    # = exatamente com
    # $ expressão regular O uso de ("$name",) é mais comum em ambientes MongoDB com suporte a djongo.
    # @ fulltext disponível apenas para PostgreSQL
    search_fields = ("^name",)
    ordering_fields = (
        "name",
        "manufacturing_date",
    )

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = "drones"
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-detail"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )

class PilotList(generics.ListCreateAPIView):
    throttle_scope = "pilots"
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-list"
    filterset_fields = (
        "gender",
        "races_count",
    )
    # o simbolo ^ indica que a busca vai retornar as instâncias dos Pilot que inicia com o name fornecido
    search_fields = ("=gender",)
    ordering_fields = ("name", "races_count")
    # autenticação baseada em token
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = "pilots"
    throttle_classes = (ScopedRateThrottle,)
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-detail"
    # autenticação baseada em token
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-list"
    filterset_class = CompetitionFilter
    ordering_fields = (
        "distance_in_feet",
        "distance_achievement_date",
    )


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-detail"
