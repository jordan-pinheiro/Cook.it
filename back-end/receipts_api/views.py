from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .models import Receipts, Category, Rating
from .serializers import ReceiptsSerializer, CategorySerializer, RatingSerializer
from .filters import ReceiptsFilter
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class ReceiptViewSet(viewsets.ModelViewSet):

    queryset = Receipts.objects.filter(status='aprovado')
    serializer_class = ReceiptsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filterset_class = ReceiptsFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, 'django_filters.rest_framework.DjangoFilterBackend']

    search_fields = ['title', 'ingredients']
    ordering_fields = ['prepare_time', 'created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, status='pending')

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        receipt = self.get_object()
        user = request.user
        if user in receipt.favorited_by.all():
            receipt.favorited_by.remove(user)
            return Response({'status': 'Receipt unfavorited'})
        else:
            receipt.favorited_by.add(user)
            return Response({'status': 'Receipt favorited'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        receipt = self.get_object()
        receipt.status = 'aprovado'
        receipt.save()
        return Response({'status': 'Receipt approved'})

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Rating.objects.filter(Receipts_id=self.kwargs['Receipts_pk'])

    def perform_create(self, serializer):
        Receipts = Receipts.objects.get(id=self.kwargs['Receipts_pk'])
        serializer.save(usuario=self.request.user, Receipts=Receipts)