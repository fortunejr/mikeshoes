from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('index/<int:id>', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('delete/', views.delete, name='delete'),
]
