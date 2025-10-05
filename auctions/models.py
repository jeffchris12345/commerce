from django.contrib.auth.models import AbstractUser
from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}: start bid - ${self.start_bid}"


class User(AbstractUser):
    favorites = models.ManyToManyField(Item, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.username}"

#class Watchlist(models.Model):
#    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="xx")
#    watched_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="xx")


class Bid(models.Model):
    pass



class Comment(models.Model):
    pass





