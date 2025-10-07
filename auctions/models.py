from django.contrib.auth.models import AbstractUser
from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bidder = models.CharField(max_length=64, null=True)
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    creator = models.CharField(max_length=64)
    onpost = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: start bid - ${self.bid_price}, created by {self.creator}"


class User(AbstractUser):
    favorites = models.ManyToManyField(Item, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.username}"

#class Watchlist(models.Model):
#    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="xx")
#    watched_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="xx")

class Bid(models.Model):
    bid_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bid_log", null=True)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_items", null=True)
    user_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_bid_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.bid_item} bid by {self.bid_user} at ${self.user_bid_price}"
    


class Comment(models.Model):
    pass





