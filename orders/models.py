from django.db import models


class Category(models.Model):
    """
    Category of a menuitem
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Item(models.Model):
    """
    An actual menuitem
    """
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    max_toppings = models.IntegerField(null=True)

    def __str__(self):
        if "pizza" in self.category.name.lower():
            pizza_type = self.category.name.split(" ")[0]
            return f"{pizza_type} {self.name} Pizza"
        return f"{self.name} {self.category}"


class Pricing(models.Model):
    """
    Pricing model for a menuitem
    """
    PRICING_TYPES = (
        ('small', 'Small'),
        ('large', 'Large'),
        ('na', 'N/A'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    pricing_type = models.CharField(max_length=50, choices=PRICING_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        if self.pricing_type != 'na':
            return f"{self.item}: ${self.price} Size: ${self.pricing_type}"
        return f"{self.item}: ${self.price}"


class Topping(models.Model):
    """
    Topping that can be added to an item
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Cart object that holds items a user is to checkout
    """
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart number {self.id}"


class CartItem(models.Model):
    """
    Item that will be included in the cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pricing = models.OneToOneField(Pricing, null=True, on_delete=models.CASCADE)
