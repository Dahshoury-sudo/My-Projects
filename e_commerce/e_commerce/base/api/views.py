from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import UnAuthenticated
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from base import models
from django.db import IntegrityError
from . serializers import ProductSerializer,RecentReviewSerializer,CartItemSerializer,WishListSerializer
from django.shortcuts import get_object_or_404

############################### Product
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_products(request):
    products = models.Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response({"products":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_info(request):
    product_id = request.data.get('product_id')
    product = models.Product.objects.get(id=product_id)
    serializer = ProductSerializer(product)
    return Response({"product":serializer.data},status=status.HTTP_200_OK)
#################################



################################# Auth
@api_view(['POST'])
@permission_classes([UnAuthenticated])
def register(request):
    email = request.data.get('email').strip()
    password1 = request.data.get('password1').strip()
    password2 = request.data.get('password2').strip()
    username = request.data.get('username').strip()

    if password1 != password2:
        return Response({"error":"passwords doesn't match"},status=status.HTTP_400_BAD_REQUEST)
    
    if models.User.objects.filter(username=username).exists():
        return Response({"error":"Registeration failed,Try again"},status=status.HTTP_400_BAD_REQUEST)
    
    if models.User.objects.filter(email=email).exists():
        return Response({"error":"Registeration failed,Try again"},status=status.HTTP_400_BAD_REQUEST)


    try:
        user = models.User.objects.create_user(
        username = username,
        email = email,
        password= password1,
        )

        return Response({"message":"user created"},status=status.HTTP_201_CREATED)
    
    except:
        return Response({"error":"error occurred try again"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
####################################



################################ Cart
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity'))
    if quantity < 0 :
        return Response({"error":"quantity can't be negative"},status=status.HTTP_400_BAD_REQUEST) 

    product = models.Product.objects.get(id = product_id)
    
    cart,cart_created = models.Cart.objects.get_or_create(customer = user)
    cart_item,item_created = models.CartItem.objects.get_or_create(cart = cart,product=product,defaults={"quantity":quantity,"price":product.final_price})

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"message":"item added to cart"},status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity'))

    if quantity < 0 :
        return Response({"error":"quantity can't be negative"},status=status.HTTP_400_BAD_REQUEST) 
    try:
        cartitem = models.CartItem.objects.get(product_id = product_id,cart__customer = user )
    except:
        return Response({"error":"Cart item not found for this user and product"},status=status.HTTP_404_NOT_FOUND)
    
    cartitem.quantity = quantity
    cartitem.save()
    return Response({"message":"cart edited successfully"},status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_item_from_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cart_item = models.CartItem.objects.get(product_id = product_id,cart__customer = user )
    except:
        return Response({"error":"Cart item not found for this user and product"},status=status.HTTP_404_NOT_FOUND)
    
    cart_item.delete()
    return Response({"message":"item deleted successfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_cart_items(request):
    user = request.user
    cart_items = models.CartItem.objects.filter(cart__customer = user).order_by('id')
    serializer = CartItemSerializer(cart_items,many=True)
    return Response({"items":serializer.data},status=status.HTTP_200_OK)
#####################################



############################# Wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_wishlist(request): 
    product_id = request.data.get('product_id')
    user = request.user
    try:
        product = models.Product.objects.get(id=product_id)
    except:
        return Response({"error":"product not found"},status=status.HTTP_404_NOT_FOUND)
    
    wishlist,created = models.WishList.objects.get_or_create(customer = user)

    if created:
        wishlist.products.add(product)
        return Response({"message":"item added to wishlist"},status=status.HTTP_200_OK)
    else:
        if wishlist.products.filter(id=product_id).exists():
            return Response({"message":"Item already in your wishlist"},status=status.HTTP_409_CONFLICT)
        else:
            wishlist.products.add(product)
            return Response({"message":"item added to wishlist"},status=status.HTTP_200_OK)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_item_from_wishlist(request):
    user = request.user
    product_id = request.data.get('product_id')
    try:
        product = models.Product.objects.get(id=product_id)
        
    except models.Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        wishlist = models.WishList.objects.get(customer=user)
        
    except models.WishList.DoesNotExist:
        return Response({"error": "Wishlist not found"}, status=status.HTTP_404_NOT_FOUND)


    if not wishlist.products.filter(id=product_id).exists():
        return Response({"error": "Item not in wishlist"}, status=status.HTTP_400_BAD_REQUEST)
    
    wishlist.products.remove(product) # auto saves no need to save maniually
    return Response({"message":"item deleted from wishlist"},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_wishlist_items(request):
    user = request.user
    wishlist = models.WishList.objects.get(customer = user)
    serializer = WishListSerializer(wishlist)
    return Response({"wishlist":serializer.data},status=status.HTTP_200_OK)
######################################


############################ Reviews
@api_view(['GET'])
@permission_classes([AllowAny])
def get_recent_reviews(request):
    reviews = models.Review.objects.all()[0:11]
    serializer = RecentReviewSerializer(reviews,many=True)
    return Response({"reviews":serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    user = request.user
    comment = request.data.get('comment')
    product_id = request.data.get('product_id')
    rating = request.data.get('rating')
    product = models.Product.objects.get(id=product_id)
    
    has_bought = True if models.Order.objects.filter(customer=user,items__product = product).exists() else False

    if has_bought:
        try:
            review = models.Review.objects.create(customer=user,comment=comment,rating=rating,product=product)
            return Response({"message":"review created successfully"},status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({"error":"you already reviewed this item"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e :
            return Response({"error": f"unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error":"you can't review an item that you didn't buy"},status=status.HTTP_400_BAD_REQUEST)
####################################



############################# Order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    # billing details
    billing_details ={
    "customer" : user,
    "full_name" : request.data.get('full_name'),
    "full_address" : request.data.get('full_address'),
    "country" : request.data.get('country'),
    "phone_number" : request.data.get('phone_number'),
    "order_notes" : request.data.get('order_notes'),
    }

    items = request.data.get('items')

    try:
        order,created = models.Order.objects.get_or_create(**billing_details)
        if not created:
            return Response({"error":"you already placed an order with these products"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ORDER CREATION ERROR:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    for order_item in items:
        product_id = order_item["product_id"]
        quantity = order_item["quantity"]
        product = models.Product.objects.get(id=product_id)
        try:
            models.OrderItem.objects.create(order = order,product = product,quantity=quantity,price=product.final_price)
        except:
            return Response({"error":"error creating the orderitem"},status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message":"order places successfully"},status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    user = request.user
    order_id = request.data.get('order_id')
    order = get_object_or_404(models.Order,id=order_id,customer=user)
    if order.customer == user:
        if order.status != 'cancelled':
            order.status = "cancelled"
            order.save()
            return Response({"message":"order cancelled"},status = status.HTTP_200_OK)
        else:
            return Response({"error":"order is already cancelled"},status =status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"error":"you can't delete someone's else order"},status = status.HTTP_403_FORBIDDEN)
###################################