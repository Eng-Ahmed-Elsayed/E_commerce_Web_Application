from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg', blank=True, upload_to='users_images')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ("Categories")



class Ad(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True, blank=False)
    pending_approval = models.BooleanField(null=False, blank=False)
    brand = models.CharField(max_length=50, null=True)
    model_year = models.IntegerField(null=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    details = models.TextField(null=True)
    img = models.ImageField(null=True, default='no-image.png', blank=True, upload_to='ads_images')
    # cart = models.ManyToManyField(Cart, null=True, blank=True, related_name='cart')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_ads = models.ManyToManyField(
        Ad, related_name='cart_ads', blank=True
    )
    def __str__(self):
        return str(self.user) + ' Cart'
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_ads = models.ManyToManyField(
        Ad, related_name='favorite_ads', blank=True
    )
    def __str__(self):
        return str(self.user) + ' Favorites'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad,  on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, null=True, blank=True)
    review = models.CharField(max_length=50, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ad) + '_' + str(self.user) + '_review'
    class Meta:
        ordering = ['-updated', '-created']







