from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

    def __str__(self):
        return f"id: {self.id}"

class Category(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Category : {self.category}"

class Listing(models.Model):
    user = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField( blank=True)
    CLOTHING = 'CLOTHING'
    FURNITURE = 'FURNITURE'
    COMPUTER = 'COMPUTER'
    APPLIANCE = 'APPLIANCE'
    '''category = [
        (CLOTHING, 'Clothing'),
        (FURNITURE, 'Furniture'),
        (COMPUTER, 'Computer and accessories'),
        (APPLIANCE, 'Appliance'),
        (None, 'No category')
    ]'''
    category = models.ForeignKey(Category, related_name='cat_listings', on_delete=models.CASCADE, null=True, blank = True)
    image = models.URLField(max_length=1000, blank=True)
    ACTIVE = 'ACTIVE'
    BIDDING = 'BID'
    CLOSED = 'CLOSED'
    STATUS = [
        (ACTIVE, 'Active'),
        (BIDDING, 'Bidding'),
        (CLOSED,'Closed')
    ]
    status = models.CharField(choices=STATUS, default=ACTIVE, max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title: {self.title} | category: {self.category}"


class Bid(models.Model):
    user = models.ForeignKey(User, related_name="user_bids", on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listing, related_name="bids", on_delete=models.CASCADE, default=1)
    bid = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user} | listing: {self.listing} | bid: {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE, default=1)
    comment = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"user: {self.user} | listing: {self.listing} | comment: {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, related_name="watchlist", on_delete=models.CASCADE, default=1)
    listing = models.ForeignKey(Listing, related_name="watching", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"user: {self.user} | listing: {self.listing}"