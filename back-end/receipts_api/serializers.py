from rest_framework import serializers
from .models import Receipts, Category, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('user',) # Define o usuário automaticamente pela view

class ReceiptSerializer(serializers.ModelSerializer):
    # Traz o nome do autor em vez de só o ID
    author_name = serializers.ReadOnlyField(source='author.username')
    # Traz as avaliações aninhadas (IC-16)
    ratings = RatingSerializer(many=True, read_only=True)
    # Calcula a média de notas (IC-16)
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Receipts
        # Inclui tudo!
        fields = [
            'id', 'title', 'ingredients', 'prepare_mode', 'prepare_time',
            'difficulty', 'author', 'author_name', 'Category', 'main_image',
            'status', 'favorited_by', 'ratings', 'rating_average'
        ]
        read_only_fields = ('author', 'status', 'favorited_by') # Campos definidos pelo backend

    def get_rating_average(self, obj):
        from django.db.models import Avg
        media = obj.ratings.aggregate(Avg('score')).get('score__avg')
        return media if media else 0