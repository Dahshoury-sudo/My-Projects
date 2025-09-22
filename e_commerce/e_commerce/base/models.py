from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.core.mail import send_mail
from dirtyfields import DirtyFieldsMixin
from django.db.models import Avg
from decimal import Decimal
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True,unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    discount = models.PositiveIntegerField(null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True,editable=False)
    stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category,related_name='products',blank=True)
    tags = models.ManyToManyField(Tag,related_name='products',blank=True)
    img = CloudinaryField("products",null=True)

    def save(self,*args,**kwargs):
        if self.discount and 0 <= self.discount <= 100:
            self.final_price = Decimal(self.original_price) * (Decimal(1)-(Decimal(self.discount)/Decimal(100)))
        else:
            self.final_price = self.original_price
        super().save(*args,**kwargs)

    @property
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    
    def __str__(self):
        return self.name

class Review(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  #1–5 stars
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "customer")  # one review per customer per product
        ordering = ["-created"]

    def __str__(self):
        return self.product.name
    

class WishList(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist')
    products = models.ManyToManyField(Product,related_name='wishlists',blank=True)

    def __str__(self):
        return self.customer.username




class Order(DirtyFieldsMixin,models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    # Biling details
    full_name = models.CharField(max_length=200,null=True)
    full_address = models.CharField(max_length=300,null=True)
    order_notes = models.TextField(null=True)
    phone_number = models.CharField(max_length=25,null=True)
    country = models.CharField(max_length=100,null=True)

    @property
    def total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())
    
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
 
    def __str__(self):
        return self.customer.username if self.customer else "Guest Cart"



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True)

    @property
    def subtotal(self): # for each item not whole order
        return self.quantity * self.price
    
    def save(self,*args,**kwargs):
        self.price = self.product.final_price
        super().save(*args,**kwargs)

    def __str__(self):
        return self.product.name        



class Payment(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payments')
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(decimal_places=2,max_digits=10)

    METHOD_CHOICES = [
        ("credit_card","Credit Card"),
        ("debit_card","Debit Card"),
        ("cash","Cash"),
        ("paypal","PayPal"),
        ("bank_transfer","Bank Transfer")
    ]

    method = models.CharField(max_length=50,choices=METHOD_CHOICES)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    transaction_id = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.customer.username if self.customer else "Guest Cart" 




class Cart(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return self.customer.username if self.customer else "Guest Cart"




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True)

    @property
    def subtotal(self): # for each item not whole cart
        return self.quantity * self.price
    
    def save(self,*args,**kwargs):
        self.price = self.product.final_price
        
        super().save(*args,**kwargs)

    def __str__(self):
        return self.product.name














####################### Signals ########################

##### Commented cuz it takes so much time and slows the web #####


# @receiver(post_save,sender=User)
# def user_post_save_receiver(sender,instance,created,*args,**kwargs):
#     if created:
#         send_mail(
#     subject="Welcome!",
#     message=f"Hey {instance.username} Thank you for signing up in our e-commerce website",
#     from_email= settings.DEFAULT_FROM_EMAIL,
#     recipient_list=[instance.email],
#     fail_silently=True,
# )
#     else:
#         print("You account information has been updated")


# @receiver(post_save,sender=Order)
# def order_post_save_receiver(sender,instance,created,*args,**kwargs):
#     if created:
#         send_mail(
#     subject="Your Order",
#     message=f"Hello {instance.customer.username}, we wanted to inform you that your order has been placed successfully",
#     from_email=settings.DEFAULT_FROM_EMAIL,
#     recipient_list=[instance.customer.email],
#     fail_silently=True,
#     )
    
#     else:
#         if "status" in instance.get_dirty_fields():
#             if instance.status == 'shipped':
#                 message = f"Hello {instance.customer.username}, you order has been shipped and will be delivered soon.\nStay Tuned"
#             elif instance.status == 'delivered':
#                 message = f"Hello {instance.customer.username}, you order has been delivered to your place"
#             elif instance.status == 'cancelled':
#                 message = f"Hello {instance.customer.username}, you order has been been cancelled"
#             elif instance.status == 'pending':
#                 message = f"Hello {instance.customer.username}, you order is now pending"
#             elif instance.status == 'paid':
#                 message = f"Hello {instance.customer.username}, you order has been paid successfully"
#             else:
#                 return
        
#         else:
#             return 
        
#         send_mail(
#     subject="Your Order",
#     message=message,
#     from_email=settings.DEFAULT_FROM_EMAIL,
#     recipient_list=[instance.customer.email],
#     fail_silently=True,
# )
