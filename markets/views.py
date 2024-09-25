from django.shortcuts import render, get_object_or_404
from .models import Market, ProductVariant, Store, Product, Category
# from .forms import ProductForm
from django.db.models import F
from django.db.models import Count, Sum
def index(request):
    market_id = request.GET.get('market_id', 0)
    store_id = request.GET.get('store_id', 0)
    product_id = request.GET.get('product_id', 0)
    category_id = request.GET.get('category_id', 0)
    market=[]
    markets=[]
    store=[]
    stores=[]
    product=[]
    products=[]
    product_variants=[]
    color_groups = {}
    total_quantity=0
    total_color=[]
    total_size=[]
    total_color_size=[]
    category=[]
    markets=Market.objects.filter(is_deleted=False).values()
    all_stores=Store.objects.filter(is_deleted=False).values()
    all_products=Product.objects.filter(is_deleted=False).values()
    categories=Store.objects.filter(is_deleted=False).values('type__id', 'type__name_en_us', 'type__name_ru_ru', 'type__name_uz_crl', 'type__name_uz_uz', 'type__sort_order').annotate(id=F('type__id'), name_en_us=F('type__name_en_us'), name_ru_ru=F('type__name_ru_ru'), name_uz_crl=F('type__name_uz_crl'), name_uz_uz=F('type__name_uz_uz'), sort_order=F('type__sort_order'), total=Count('type__id')).values('id', 'name_en_us', 'name_ru_ru', 'name_uz_crl', 'name_uz_uz', 'sort_order',   'total')
    if int(market_id) > 0:
        market=Market.objects.filter(id=market_id).values().first()
    if int(store_id) == 0:
        stores=Store.objects.filter(is_deleted=False, market_id=market_id).values()
    else:
        store=Store.objects.filter(id=store_id).values().first()
        market_id=Store.objects.filter(id=store_id).values_list('market_id')[0][0]
        market=Market.objects.filter(id=market_id).values().first()
    if int(product_id) == 0:
        products=Product.objects.filter(is_deleted=False, store_id=store_id).values()
    else:
        # product_variants=ProductDetail.objects.filter(product_id=product_id).annotate(size_name=F('size__name'), size_description=F('size__description'), size_code=F('size__code'), size_value=F('size__value'), size_count=Count('size__value'), color_count=Count('color')).values()
        product_variants=ProductVariant.objects.filter(product_id=product_id).annotate(size_value=F('size__value'), size_count=Count('size__id')).values()
        product=Product.objects.filter(id=product_id).values().first()
        variants=ProductVariant.objects.filter(product_id=product_id)

        total_quantity=variants.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_color=variants.values('color').annotate(total_color=Sum('quantity'))
        total_size=variants.values('size__value').annotate(size=F('size__value'), total_size=Sum('quantity')).values('size', 'total_size')
        total_color_size=variants.values('color', 'size__value').annotate(size=F('size__value'), total=Sum('quantity')).values('color', 'size', 'total')
        store_id=Product.objects.filter(id=product_id).values_list('store_id')[0][0]
        store=Store.objects.filter(id=store_id).values().first()
        market_id=Store.objects.filter(id=store_id).values_list('market_id')[0][0]
        market=Market.objects.filter(id=market_id).values().first()
    context={
        'market_id':market_id,
        'market': market,
        'markets':markets,
        'store_id':store_id,
        'store': store,
        'stores': stores,
        'all_stores': all_stores,
        'product_id':product_id,
        'product': product,
        'products': products,
        'all_products': all_products,
        'product_variants': product_variants,
        'color_groups': color_groups,
        'total_quantity': total_quantity,
        'total_color': total_color,
        'total_size': total_size,
        'total_color_size': total_color_size,
        'category_id':category_id,
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
