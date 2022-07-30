from django.shortcuts import render
from django.core.paginator import Paginator
from store.models import *


def show_products(request):
    products = Product.objects.all()
    p = Paginator(Product.objects.all(), 5)
    page = request.GET.get('page')
    prds = p.get_page(page)
    nums = "a" * prds.paginator.num_pages
    return render(request, 'show_products.html', {'products':products, 'prds':prds, 'nums':nums})
