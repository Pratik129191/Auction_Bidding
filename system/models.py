from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Auction(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='system/images')

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    offer = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.user} {self.status}"


class AuctionBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    offer = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']

    def __str__(self):
        return f"{self.offer} - {self.user}"

