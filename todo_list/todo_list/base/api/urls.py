from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/',views.register),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',views.logout),
    path('task/add/',views.addtask),
    path('task/all/',views.getusertasks),
    path('task/get/<str:pk>',views.gettask),
    path('task/edit/<str:pk>',views.edittask),
    path('task/delete/',views.deletetask),
    path('task/complete/',views.completetask),

]