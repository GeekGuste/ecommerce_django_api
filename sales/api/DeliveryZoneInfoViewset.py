from rest_framework.viewsets import ModelViewSet
from sales.models import DeliveryZoneInfo
from sales.serializers import DeliveryZoneInfoSerializer

class DeliveryZoneInfoViewset(ModelViewSet):
    serializer_class = DeliveryZoneInfoSerializer
    def get_queryset(self):
        queryset = DeliveryZoneInfo.objects.all()
        return queryset