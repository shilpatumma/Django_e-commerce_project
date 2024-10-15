from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import SignupForm
from django.contrib import messages


#  product_list View...

def product_list(request):
    """
        Displays a list of available products with search and category
        filter functionality.
    """
    
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Category filter
    category_slug = request.GET.get('category')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)


    # Pagination
    paginator = Paginator(products, 6) # Show 6 products per page
    page = request.GET.get('page')
    
    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    context = {
        'products': products_paginated,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'store/product_list.html', context)



#  product_detail View...

def product_list(request, id, slug):
    """
        Displays detailed information about a specific product.
    """
    
    product = get_object_or_404(Product, id = id, slug = slug, available = True)
    return render(request, 'store/product_detail.html', {'product': product})
    
    
    