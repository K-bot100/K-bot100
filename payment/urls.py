from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [  
       
    path('api/payments', views.Paymentslist.as_view()), #api view when using django rest framework

     path('payment/',views.payment, name='payment' ),
    
     path('payments/',views.history, name='history' ),
     path('', views.userLogin.as_view(), name="login"),

    path('logout/', auth_views.LogoutView.as_view(), name = 'logout')

]