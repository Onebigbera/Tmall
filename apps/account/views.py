from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

"""
    购物车相关操作肯定是在用户登陆的前提下擦操作的
    查看购物车商品和付款|添加商品等
"""


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        # 多做判断是判断一个程序员好坏的标准之一
        if username and password:
            # 相当于用户登陆| 不判断激活状态
            user = authenticate(username=username, password=password)
            # 用户存在
            if user:
                # 判断用户状态
                # 激活 | 未激活 | 删除
                if user.is_active:
                    # 记住用户的登陆状态 保持登陆状态
                    login(request, user)
                    return redirect('/')
                else:
                    # 用户未激活
                    pass
            else:
                # 用户账户密码错误
                return render(request, 'login.html')
        else:
            # 关键字段不能为空
            pass
    return render(request, 'login.html')


def register(request):
    pass


def logout(request):
    pass
