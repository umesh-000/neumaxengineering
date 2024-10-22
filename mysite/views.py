from django.core.paginator import Paginator
from myadmin import models as adminmodels
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models import Q
from accounts import models as accountmMdels
from django.http import JsonResponse
from django.contrib import messages

def home(request):
    context = {
        
    }
    return render(request, 'site_master.html', context)


def about(request):

    if request.user.is_authenticated:
       pass

    context = {
        
    }
    return render(request, 'mysite/about_us.html',context)


def contact(request):

    if request.user.is_authenticated:
       pass

    context = {
      
    }
    return render(request, 'mysite/contact_us.html', context)



def terms_conditions(request):

    if request.user.is_authenticated:
       pass

    context = {
        
    }
    return render(request, 'mysite/terms_and_conditions.html', context)


def shop_catalog(request):
    
    if request.user.is_authenticated:
       pass

    context = {
      
    }
    return render(request, 'mysite/shop_catalog.html', context)


def product_details(request, id):
    
    if request.user.is_authenticated:
        pass

    context = {
        
    }
    return render(request, 'mysite/product_details.html', context)


def category_products(request, id):
   
    
    context = {
    
    }
    return render(request, 'mysite/category_products.html', context)