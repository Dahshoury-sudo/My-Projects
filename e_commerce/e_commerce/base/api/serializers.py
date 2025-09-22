from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import Product,Review,WishList,CartItem,OrderItem

class ProductSerializer(ModelSerializer):
    img_url = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)  # comes from @property
    categories = serializers.StringRelatedField(many=True)  # uses __str__ from Category
    tags = serializers.StringRelatedField(many=True)   # uses __str__ from Tag
    class Meta:
        model = Product
        exclude = ['img']
    
    def get_img_url(self, obj):
        return obj.img.url if obj.img else None

class ProductSerializerForWishlist(ModelSerializer):
    average_rating = serializers.FloatField(read_only = True)
    img_url = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['final_price','original_price','discount','img_url','average_rating','product_id']
    
    def get_product_id(self,obj):
        return obj.id if obj else None

    def get_img_url(self, obj):
        return obj.img.url if obj.img else None

class WishListSerializer(ModelSerializer):
    products = ProductSerializerForWishlist(many=True,read_only = True)
    class Meta:
        model = WishList
        fields = "__all__"


class RecentReviewSerializer(ModelSerializer):
    customer = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = '__all__'



class CartItemSerializer(ModelSerializer):
    subtotal = serializers.FloatField(read_only = True)
    product_name = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        exclude = ['product','cart','id']
    
    def get_product_name(self,obj):
        return obj.product.name if obj.product else None
    
    def get_img_url(self,obj):
        return obj.product.img.url if obj.product.img else None
    
    def get_product_id(self,obj):
        return obj.product.id if obj.product else None
