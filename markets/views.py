from django.shortcuts import render, get_object_or_404
from .models import Market, Store, Product, Category
from .forms import ProductForm
from django.db.models import F
from django.db.models import Count
def index(request):
    id = request.GET.get('id', 0)
    market_id = request.GET.get('market_id', 0)
    store_id = request.GET.get('store_id', 0)
    category_id = request.GET.get('category_id', 0)
    market=[]
    store=[]
    category=[]
    categories=Store.objects.filter(is_deleted=False).values('category__id', 'category__name_en_us', 'category__name_ru_ru', 'category__name_uz_crl', 'category__name_uz_uz', 'category__sort_order').annotate(id=F('category__id'), name_en_us=F('category__name_en_us'), name_ru_ru=F('category__name_ru_ru'), name_uz_crl=F('category__name_uz_crl'), name_uz_uz=F('category__name_uz_uz'), sort_order=F('category__sort_order'), total=Count('category__id')).values('id', 'name_en_us', 'name_ru_ru', 'name_uz_crl', 'name_uz_uz', 'sort_order',   'total')
    if market_id == 0:
        markets=Market.objects.filter(is_deleted=False).values()
    else:
        market=Market.objects.filter(id=market_id).values().first()
    if store_id == 0:
        stores=Store.objects.filter(is_deleted=False, market_id=market_id).values()
    else:
        store=Store.objects.filter(id=store_id).values()
    if category_id == 0:
        stores=Store.objects.filter(is_deleted=False).values()
    else:
        category=Category.objects.filter(id=category_id).values().first()
        stores=Store.objects.filter(type=category_id).values()
    context={
        'id':id,
        'market': market,
        'markets':markets,
        'category':category,
        'categories':categories.order_by('-sort_order'),
    }
    return render(request, 'markets/index.html', context=context)
def market_list(request):
    markets = Market.objects.all()
    return render(request, 'markets/market_list.html', {'markets': markets})

def store_list(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    stores = Store.objects.filter(market=market)
    return render(request, 'markets/store_list.html', {'market': market, 'stores': stores})

def product_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    return render(request, 'markets/product_list.html', {'store': store, 'products': products})
