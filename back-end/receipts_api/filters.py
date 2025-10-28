from django_filters import rest_framework as filters
from .models import Receipt

class ReceiptsFilter(filters.FilterSet):
    # IC-03 (Busca por category):
    # Cria um filtro '.../?category=2'
    category = filters.NumberFilter(field_name='category__id')
    
    # IC-15 (Tempo de preparo):
    # 'RangeFilter' cria DOIS parâmetros:
    # '.../?prepare_time_min=10' e '.../?prepare_time_max=30'
    prepare_time = filters.RangeFilter()
    
    # IC-15 (Dificuldade):
    # 'lookup_expr='iexact'' torna o filtro case-insensitive.
    # '.../?difficulty=facil' funciona.
    difficulty = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Receipt
        # Lista de campos que o django-filter deve usar
        fields = ['category', 'prepare_time', 'difficulty']