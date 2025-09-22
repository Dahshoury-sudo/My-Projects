from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Payment)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Product)
admin.site.register(models.Review)
admin.site.register(models.WishList)
admin.site.register(models.Tag)
