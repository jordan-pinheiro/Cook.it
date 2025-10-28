from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer
# Create your views here.

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]