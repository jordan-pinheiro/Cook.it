from django.db import models
from django.contrib.auth.models import User

class Category(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Receipt(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
    )

    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    prepare_mode = models.TextField()
    prepare_time = models.IntegerField()
    difficulty = models.CharField(max_length=50)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='receipts') # IC-06

    main_image = models.ImageField(upload_to='receipts_imgs/', blank=True, null=True) # IC-07
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') # IC-17
    
    # IC-12 (Favoritos)
    favorited_by = models.ManyToManyField(User, related_name='favorited_receipts', blank=True)

    def __str__(self):
        return self.title

class Rating(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)