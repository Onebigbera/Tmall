from django.shortcuts import render

from apps.home.models import Shop


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        # 根据关键字获取商品对象
        shops = Shop.objects.filter(name__contains=keyword)
        for shop in shops:
            # 获取每个商品得图片并且将其与商品绑定
            # 遍历包含关键字的商品 将其与之对应的照片得到动态绑定到其属性上
            shop.image = shop.shopimage_set.filter(type='type_single').first()
        return render(request, 'search.html', {'shops': shops})

    else:
        return render(request, 'error/error_400.html')
