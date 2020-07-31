from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    starting_bid = models.FloatField()
    current_price = models.FloatField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="winner", null=True, blank=True)
    date_created = models.DateTimeField()
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    bid = models.FloatField(default=0)
    latest_bid_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return f"{self.listing}: ${self.bid} created {self.latest_bid_time}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    comment = models.TextField(default=None)
    time = models.DateTimeField()
    def __str__(self):
        return f"'{self.comment}' by {self.user}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return f" {self.user}: {self.listing}"


