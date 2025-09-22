from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/',views.register),
    path('auth/logout/',views.logout),

    # Product
    path('products/',views.get_all_products),
    path('products/get/',views.get_product_info),
    
    # Cart
    path('cart/add/',views.add_item_to_cart),
    path('cart/remove/',views.remove_item_from_cart),
    path('cart/edit/',views.edit_cart),
    path('cart/items/',views.show_cart_items),

    # Order
    path('order/add/',views.place_order),
    path('order/cancel/',views.cancel_order),

    # Wishlist
    path('wishlist/add/',views.add_item_to_wishlist),
    path('wishlist/remove/',views.remove_item_from_wishlist),
    path('wishlist/items/',views.show_wishlist_items),

    # Review
    path('reviews/recent/',views.get_recent_reviews),
    path('reviews/add/',views.add_review),

]
