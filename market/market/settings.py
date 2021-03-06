"""
Django settings for market project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR ,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r7@m*n+o&$rvsi52@g!1u#oh!v78j_q6gcb8(%)fij0z&4&dvz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',  # 全文检索框架
    # 添加子应用
    'user.apps.UserConfig',
    'goods.apps.GoodsConfig',
    'order.apps.OrderConfig',
    'cart.apps.CartConfig',
    # 添加ckeditor富文本编辑器
    'ckeditor',
    # 添加ckeditor富文本编辑器文件上传部件
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'market.urls'

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
                'django.template.context_processors.media', #添加渲染 MEDIA_URL 变量
            ],
        },
    },
]

WSGI_APPLICATION = 'market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR,'my.cnf')
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
# 设置静态文件根目录  上线的时候使用
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


#添加django中的缓存配置
#徐挂起redis服务器，1代表1号数据库
CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


#修改默认sessioin的存储引擎
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 配置短信需要的key
ACCESS_KEY_ID = "LTAI2qSiJdWP87em"
ACCESS_KEY_SECRET = "FzORQ587PgGBoOAdmxzCjaxQi8klUi"

# 配置上传图片
MEDIA_URL = "/static/media/"
# 配置该URL对应的物理目录存储地址
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
#配置ckeditor 相对  MEDIA_ROOT
CKEDITOR_UPLOAD_PATH = "uploads/"
# 编辑器样式配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
#配置搜索引擎
# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 配置搜索引擎 修改成自己配置的搜索引擎
        'ENGINE': 'utils.whoosh_cn_backend.WhooshEngine',
        # 配置索引文件目录
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
#显示每页条数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50