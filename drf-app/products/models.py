from django.db import models
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

class Product(BaseModel):
    
    CATEGORY_CHOICES = [
        ('ELEC', 'Eletrônicos'),
        ('FASH', 'Moda'),
        ('HOME', 'Casa'),
        ('FOOD', 'Alimentos'),
        ('OTHR', 'Outros'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} - R$ {self.price:.2f}"
