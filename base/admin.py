from django.contrib import admin
from .models import User, Ad, Favorite, Category, Cart, Review
# Register your models here.

admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Favorite)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Review)

