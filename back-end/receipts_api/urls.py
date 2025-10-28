from django.urls import path, include
from rest_framework_nested import routers # pip install drf-nested-routers
from . import views

router = routers.DefaultRouter()
router.register(r'receipts', views.ReceiptsViewSet, basename='receipts')
router.register(r'categorys', views.CategoryViewSet, basename='categorys')

# Rota aninhada para avaliações: /api/receipts/1/rate/
receipts_router = routers.NestedSimpleRouter(router, r'receipts', lookup='receipts')
receipts_router.register(r'rate', views.RatingViewSet, basename='receipts-rate')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(receipts_router.urls)),
]