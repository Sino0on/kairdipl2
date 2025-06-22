from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=123, blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=123, blank=True, null=True)
    pic = models.FileField(upload_to="images")
    price = models.CharField(max_length=123)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Продукт'

