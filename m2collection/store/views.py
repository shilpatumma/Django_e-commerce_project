from django.shortcuts import render, redirect,  get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
# from django.contrib.auth import login 
from django.contrib.auth import logout



#  product_list View...

# def product_list(request):
#     """
#         Displays a list of available products with search and category
#         filter functionality.
#     """
    
#     products = Product.objects.filter(available=True)
#     categories = Category.objects.all()
    
#     # Search functionality
#     query = request.GET.get('q')
    
#     if query:
#         products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

#     # Category filter
#     category_slug = request.GET.get('category')
    
#     if category_slug:
#         products = products.filter(category__slug=category_slug)


#     # Pagination
#     paginator = Paginator(products, 6) # Show 6 products per page
#     page = request.GET.get('page')
    
#     try:
#         products_paginated = paginator.page(page)
#     except PageNotAnInteger:
#         products_paginated = paginator.page(1)
#     except EmptyPage:
#         products_paginated = paginator.page(paginator.num_pages)

#     context = {
#         'products': products_paginated,
#         'categories': categories,
#         'query': query,
#         'selected_category': category_slug,
#     }
#     return render(request, 'store/product_list.html', context)



# #  product_detail View...

# def product_list(request, id, slug):
#     """
#         Displays detailed information about a specific product.
#     """
    
#     product = get_object_or_404(Product, id = id, slug = slug, available = True)
#     return render(request, 'store/product_detail.html', {'product': product})
    
    
    
    
def product_list(request):
    """
    Displays a list of available products with search and category filter functionality.
    """
    # Retrieve all available products
    products = Product.objects.filter(available=True)
    
    # Get all categories for filtering
    categories = Category.objects.all()

    # Search functionality: Filter products by name or description
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Category filter: Filter products by selected category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Pagination: Show 6 products per page
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    # Context to pass to the template
    context = {
        'products': products_paginated,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }
    
    # Render the product list template
    return render(request, 'store/product_list.html', context)
    
    
       
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('store:login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Logs the user out  
        return render(request, 'blog/post_list.html')  # type: ignore # Redirect to the post list or any other page
    else:
        return render(request, 'registration/logout.html')  # If GET, redirect to a safe page