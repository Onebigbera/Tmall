import os

# 项目的根目录
import sys

# 定位到当前路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR) # F:\Django_twice\Training_Projects\Tmall

# 加密的密钥  用户系统 | session
SECRET_KEY = 'x=!u#0hu@c=6j@25d5&$72t=y5yhm_u*@je+8qe=9zh3_7cy7p'

# 开发的时候用的  上线部署的时候改为False
DEBUG = True

# 允许访问的ip地址 默认设置所有的ip地址都能访问
ALLOWED_HOSTS = []

# 系统自带APPS
SYS_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 将app进行拆分 用户的apps
CUSTOM_APPS = [
    'apps.home',
    'apps.search',
    'apps.account',
    'apps.cars',
    'apps.order',

]

# 外部扩展的apps
EXT_APPS = [
    # 核心
    'xadmin',
    # 后台更改显示相关
    'crispy_forms',
    # 主题相关的app
    'reversion',
]

# 列表相加 解耦思想 便于管理apps
INSTALLED_APPS = SYS_APPS + CUSTOM_APPS + EXT_APPS

# 中间件注册
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 默认的根url配置 项目的url
ROOT_URLCONF = 'Tmall.urls'

# 模板相关的配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 项目部署相关
WSGI_APPLICATION = 'Tmall.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tmall_twice',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
        'CHARSET': 'utf-8',
    }
}

# 用户认证密码
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 语言设置
LANGUAGE_CODE = 'zh-hans'

# 时区
TIME_ZONE = 'Asia/Shanghai'

# USE internationalization
USE_I18N = True

# use language_code
USE_L10N = True

# use timezone
USE_TZ = True

# 静态文件路径和根目录
STATIC_URL = '/static/'

# 元祖形式存放 注意加 ','
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# print(STATICFILES_DIRS)

# 上传文件访问的根路径
MEDIA_URL = '/media/'

# 配置上传文件的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django_redis.cache.RedisCache
# 缓存的配置 这里用Redis数据库存储缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'TIMEOUT': 300,
        'OPTIONS': {
            'PASSWORD': '123456',
        }
    }
}

# 设置redis存储session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 解决在app中导入模块时 模块中模型定位不明确的问题解决方法 将此项目中apps目录添加到BASE_DIR中
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# session默认的相关配置

# 用户认证相关
# 修改模块内的用户授权系统
# 并没有重写用户认证的类
# AUTH_USER_MODEL = 'apps.home.User'
LOGIN_URL = '/account/login/'

# 待完善模块
# 发送邮件相关配置

# AliPay相关配置
