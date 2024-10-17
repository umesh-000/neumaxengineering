from django.contrib import admin
from django.urls import path
from myadmin import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('<int:id>/profile_details', views.admin_profile_details, name='admin_profile_details'),
    path('<int:id>/change_password', views.admin_change_password, name='admin_change_password'),


    # Category
    path('categories/', views.categories, name='categories_list'),
    path('categories/create/', views.categories_create, name='categories_create'),
    path('categories/<int:id>/edit', views.categories_edit, name='categories_edit'),
    path('categories/<int:id>/delete', views.categories_delete, name='categories_delete'),

    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.products_create, name='products_create'),
    path('products/<int:id>/edit', views.products_edit, name='products_edit'),
    path('products/<int:id>/delete', views.products_delete, name='products_delete'),

]
