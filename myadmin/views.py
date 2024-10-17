from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from accounts import models as  account_models
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from myadmin import models
from myadmin import utils
import logging

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()  # Get the custom user model

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    # Check if the user session exists (handled by middleware)
    if not request.admin_user:
        return redirect('login')

    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/dashboard.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_profile_details(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    admin_profile = get_object_or_404(account_models.Admins, id=id)
    
    context = {
        'admin_user': request.user,
        'admin_profile': admin_profile,
    }
    return render(request, 'admin/admin_profile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_change_password(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    admin_profile = get_object_or_404(account_models.Admins, id=id)
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = admin_profile.user
        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('admin_profile_details', id=id)

        # Check if new passwords match
        if new_password != confirm_new_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('admin_profile_details', id=id)

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Update session so the user isn't logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('admin_profile_details', id=id)

    context = {
        'admin_user': request.user,
        'admin_profile': admin_profile,
    }
    return render(request, 'admin/admin_profile.html', context)


# Categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories(request):
    if not request.admin_user:
        return redirect('login')
    categories = models.Category.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'admin_user': request.admin_user,
        'categories': page_obj,
    }
    return render(request, 'admin/categories_list.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories_create(request):
    if not request.admin_user:
        return redirect('login')
    
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('file')
        # Create the category
        try:
            category = models.Category.objects.create(
                name=name,
                description=description,
                status=status,
                image=image,
            )
            messages.success(request, 'Category created successfully!')
            return redirect('categories_list')
        except Exception as e:
            messages.error(request, f'Error creating category: {str(e)}')
    
    context = {
        'admin_user': request.admin_user,
    }
    return render(request, 'admin/categories_create.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories_edit(request, id):
    if not request.admin_user:
        return redirect('login')

    category = get_object_or_404(models.Category, id=id)

    if request.method == 'POST':
        # Handle form submission
        category.name = request.POST.get('title')
        category.status = request.POST.get('status')
        category.description = request.POST.get('description')
        # Handle file upload if a new file is provided
        if request.FILES.get('file'):
            category.image = request.FILES['file'] 

        category.save()
        messages.success(request, 'Category Updated successfully!')
        return redirect('categories_list')

    context = {
        'admin_user': request.admin_user,
        'category': category,
    }
    return render(request, 'admin/categories_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categories_delete(request, id):
    if request.method == 'POST':
        try:
            if not request.admin_user:
                return redirect('login')
            category = get_object_or_404(models.Category, id=id)
            category.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# Products
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products_list(request):
    if not request.admin_user:
        return redirect('login')
    
    products = models.Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'admin_user': request.admin_user,
        'products': page_obj,
    }
    return render(request, 'admin/products_list.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products_create(request):
    if not request.admin_user:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(models.Category, id=category_id)
        # Images and Videos
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        # Generate a unique SKU
        sku = utils.generate_unique_sku()

        # Create the product
        try:
            product = models.Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock=stock,
                sku=sku,  # Using the generated SKU
                status=status,
                category=category
            )
            # Save product images
            for image in images:
                models.ProductImage.objects.create(product=product, image=image)

            # Save product videos
            for video in videos:
                models.ProductVideo.objects.create(product=product, video=video)

            messages.success(request, 'Product created successfully!')
            return redirect('products_list')

        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')

    context = {
        'admin_user': request.admin_user,
        'categories': models.Category.objects.all(),
    }
    return render(request, 'admin/products_create.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products_edit(request, id):
    if not request.admin_user:
        return redirect('login')

    product = get_object_or_404(models.Product, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        category_id = request.POST.get('category_id')
        category = get_object_or_404(models.Category, id=category_id)

        # Images and Videos
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        # Update the product details
        try:
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.status = status
            product.category = category
            product.save()

            # Update images
            if images:
                product.images.all().delete()  # Remove old images
                for image in images:
                    models.ProductImage.objects.create(product=product, image=image)

            # Update videos
            if videos:
                product.videos.all().delete()  # Remove old videos
                for video in videos:
                    models.ProductVideo.objects.create(product=product, video=video)

            messages.success(request, 'Product updated successfully!')
            return redirect('products_list')

        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    context = {
        'admin_user': request.admin_user,
        'product': product,
        'categories': models.Category.objects.all(),
    }
    return render(request, 'admin/products_edit.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products_delete(request, id):
    if request.method == 'POST':
        try:
            if not request.admin_user:
                return redirect('login')
            product = get_object_or_404(models.Product, id=id)
            product.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})