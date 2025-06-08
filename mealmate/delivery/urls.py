from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signin', views.sign_in, name='signin'),
    path('signup', views.sign_up, name='signup'),
    path('customer_home/<str:username>', views.customer_home, name='customer_home'),
    path('add_restaurant', views.add_restaurant, name='add_restaurant'),
    path('restaurant_success', views.restaurant_success, name='restaurant_success'),
    path('show_restaurants', views.show_restaurants, name='show_restaurants'),
    path('update_restaurant/<int:id>', views.update_restaurant, name='update_restaurant'),
    path('delete_restaurant/<int:id>', views.delete_restaurant, name='delete_restaurant'),
    path('update_menu/<int:id>', views.update_menu, name='update_menu'),
    path('view_menu/<int:id>/<str:username>', views.view_menu, name='view_menu'),
    path('add_to_cart/<int:id>/<str:username>', views.add_to_cart, name='add_to_cart'),
    path('view_cart/<str:username>', views.view_cart, name='show_cart'),
    path('place_order/<str:username>', views.place_order, name='place_order')
]