from django.shortcuts import render, get_object_or_404
from .models import Market, Store, Product
from .forms import ProductForm

def market_list(request):
    markets = Market.objects.all()
    return render(request, 'market/market_list.html', {'markets': markets})

def store_list(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    stores = Store.objects.filter(market=market)
    return render(request, 'market/store_list.html', {'market': market, 'stores': stores})

def product_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'market/product_list.html', {'store': store, 'products': products})
