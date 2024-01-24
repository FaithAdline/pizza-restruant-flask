from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    # Add other restaurant fields as needed

class Pizza(models.Model):
    name = models.CharField(max_length=255)
    # Add other pizza fields as needed

class RestaurantPizza(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    
    # Add a price field with validation
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(1, message="Price must be at least 1."),
            MaxValueValidator(30, message="Price must be at most 30.")
        ]
    )
    
    # You can add additional fields related to the relationship if needed
    # For example, you might want to store the quantity available, etc.

    class Meta:
        unique_together = ('restaurant', 'pizza')

# Add __str__ methods for better representation in the admin interface
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    # Add other restaurant fields as needed

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=255)
    # Add other pizza fields as needed

    def __str__(self):
        return self.name

class RestaurantPizza(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    
    # Add a price field with validation
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(1, message="Price must be at least 1."),
            MaxValueValidator(30, message="Price must be at most 30.")
        ]
    )
    
    # You can add additional fields related to the relationship if needed
    # For example, you might want to store the quantity available, etc.

    class Meta:
        unique_together = ('restaurant', 'pizza')

    def __str__(self):
        return f"{self.restaurant} - {self.pizza}"
