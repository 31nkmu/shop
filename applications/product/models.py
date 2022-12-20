from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.SlugField(max_length=30, primary_key=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    descriptions = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
