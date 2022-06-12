from django.urls import path
from .views import (
    userProfile,
    deleteMessage,
    home,
    registerPage
    ,room,
    create_room,
    updatedRoom,
    deleteRoom,
    loginPage,
    logoutPage,
    registerPage,
    updateUser,
    topicsPage,
    activityPage
    )


urlpatterns = [
    path('login/',loginPage,name='loginPage'),
    path('register/',registerPage,name='registerPage'),
    path('logout/',logoutPage,name='logoutPage'),
    path('',home,name='home'),
    path('room/<str:pk>/',room,name='room'),
    path('profile/<str:pk>/',userProfile,name='userProfile'),
    path('create_room/',create_room,name = 'create_room'),
    path('update_room/<str:pk>/',updatedRoom,name = 'updatedRoom'),
    path('delete_room/<str:pk>',deleteRoom,name='deleteRoom'),
    path('delete_message/<str:pk>',deleteMessage,name='deleteMessage'),
    path('update-user/',updateUser,name='updateUser'),
    path('topics/',topicsPage,name='topicsPage'),
    path('activity/',activityPage,name='activityPage'),
]

