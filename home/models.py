from django.db import models

class New_user(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class New_product(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    cost_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    manufacturer = models.CharField(max_length=255)
    batch_number = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name