from .models import HotProduct, Categories


def hot_products(request):
    hot_products = HotProduct.objects.select_related('product')
    return {'hot_products': hot_products}

def categories_processor(request):
    return {
        'navbar_categories': Categories.objects.prefetch_related('types').all()
    }
