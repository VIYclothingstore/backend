from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserCreateSerializer, UserRetrieveUpdateDestroySerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateDestroySerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Arrrrr, you shall not pass!!!!")
        return super().delete(request, *args, **kwargs)
