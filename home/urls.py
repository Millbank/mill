
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_user.html', views.new_user, name='new_user'),
    path('home.html', views.home, name='home'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('stock_update.html', views.stock_update, name= 'stock_update')

]
