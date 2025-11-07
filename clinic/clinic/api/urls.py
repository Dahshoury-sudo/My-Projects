from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
# Auth
path('auth/register/',views.register),
path('auth/login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
path('auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

# Appointment
path('appointment/book/',views.book_appointment),
path('appointment/cancel/<str:pk>/',views.cancel_appointment),
path('appointment/all/',views.get_all_appointments),
path('appointment/stat/',views.get_all_appointments_stat),
path('appointment/schedule/<str:pk>/',views.schedule_appointment),
path('appointment/info/<str:pk>/',views.appointment_info),

# User
path('user/info/',views.user_info),


# Doctors
path('doctors/all/',views.get_all_doctors),
]