from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('register',register,name="register"),
    path('login_view',login_view,name="login_view"),
    path('logout_view',logout_view,name="logout_view"),
    path('token',token,name="token"),
    path('verify/<str:auth_token>',verify,name="verify"),
    path('error',error_page,name="error"),

]