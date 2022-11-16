from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_page),
    path("search", views.search_product),
    path('product/<str:name>/<int:pk>', views.current_product),
    path('category/<int:pk>/', views.category_product),
    path('add_product/<int:pk>', views.add_product_to_user_cart),
    path('cart', views.cart_product),
    path("delete-product/<int:pk>", views.delete_product_from_cart),
    path("send-to-tg", views.confirm_order)
    ]