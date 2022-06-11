from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UpdateUserSerializer

class UserViewset(ModelViewSet):
    serializer_class = UpdateUserSerializer
    def get_queryset(self):
        users = User.objects.all()
        #get only current user for security mesure
        users = User.objects.filter(id = self.request.user.id)
        return users