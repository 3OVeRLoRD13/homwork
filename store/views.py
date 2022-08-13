from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *


# Show products via function based view ---------------------------------------------------------------------
def show_products(request):
    products = Product.objects.all()
    p = Paginator(Product.objects.all(), 6)
    page = request.GET.get('page')
    prds = p.get_page(page)
    nums = "a" * prds.paginator.num_pages
    return render(request, 'store/show_products.html', {'products': products, 'prds': prds, 'nums': nums})


# Detail of products via function based view ----------------------------------------------------------------
def show_detail_of_product(request, pg, pk):
    detail_of_product = get_object_or_404(Product, id=pk)
    total_likes = detail_of_product.total_likes()
    current_page = pg
    liked = False
    if detail_of_product.likes.filter(id=request.user.id).exists():
        liked = True

    return render(request, 'store/show_detail_of_product.html', {'detail_of_product': detail_of_product,
                                                                 'current_page': current_page,
                                                                 'total_likes': total_likes,
                                                                 'liked': liked})


# Like product via function based view ----------------------------------------------------------------------
def like_product(request, pg, pk):
    liked_product = get_object_or_404(Product, id=request.POST.get('product_id'))
    liked = False

    if liked_product.likes.filter(id=request.user.id).exists():
        liked_product.likes.remove(request.user)
        liked = False
    else:
        liked_product.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('show_detail_of_product', args=[str(pk), str(pg)]))
