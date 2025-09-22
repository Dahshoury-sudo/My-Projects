from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('',views.home, name = "home"),
path('room/<int:pk>',views.room,name = "room"),
path('create-room/',views.createroom,name = "create-room"),
path('update-room/<int:pk>',views.updateroom,name = "update-room"),
path('delete-room/<int:pk>',views.deleteroom,name = "delete-room"),
path('delete-message/<int:pk>',views.deletemessage,name = "delete-message"),
path('update-user/',views.updateuser,name = "update-user"),
path('login/',views.loginpage,name='login'),
path('logout/',views.logoutuser,name = 'logout'),
path('register/',views.registerpage,name = 'register'),
path('profile/<int:pk>',views.userprofile,name='user-profile'),
path('topics/',views.topicspage,name='topics'),
path('activity/',views.activitypage,name='activity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

