import uuid

from django.contrib.auth import get_user_model
from django.db import models

from applications.product.models import Product

User = get_user_model()


class Order(models.Model):
    ORDER_STATUS = (
        ('in_processing', 'in_processing'),
        ('completed', 'completed'),
        ('declined', 'declined'),
    )
    owner = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=ORDER_STATUS, null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=1)
    number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    activation_code = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    address = models.CharField(max_length=60)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.product.price
        return super().save(*args, **kwargs)
