"""mei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mm import views as mm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', mm.index,name='index'),
    path('', mm.home,name='home'),
    path('send/', mm.send,name='send'),
    path('upload_img',mm.upload_img,name='upload_img'),
    path('single',mm.single,name='single'),
    path('login',mm.loginPage,name='login'),   #登录页面
    path('loginValidation',mm.loginValidation,name='loginValidation'),  #验证
    path('registration',mm.registration,name='registration'),#注册
    path('logoutPage',mm.logoutPage,name='logoutPage'),
    path('collect',mm.collect,name='collect'),  #收藏
    # admin
    path('admin/attention',mm.attention,name='attention'),
    path('admin/m_classify',mm.m_classify,name='m_classify'),
    path('admin/add_classify2',mm.add_classify2,name='add_classify2'),
    path('admin/delete_c',mm.delete_c,name='delete_c'),
    path('admin/delete_collect',mm.delete_collect,name='delete_collect'),
    path('admin/delete_myart',mm.delete_myart,name='delete_myart'),
    path('admin/set_hot',mm.set_hot,name='set_hot'),
    path('admin/my_article',mm.my_article,name='my_article'),
    path('admin/hot_manage',mm.hot_manage,name='hot_manage'),
    path('admin/my_info',mm.my_info,name='my_info'),
    path('admin_upload_s',mm.admin_upload_s,name='admin_upload_s'),
    path('change_fm',mm.change_fm,name='change_fm'),
    # 随机
    path('random_img',mm.random_img,name='random_img'),
        # 熱門
    path('hot_art',mm.hot_art,name='hot_art'),
    #分享
    path('share_meng_girl',mm.share_meng_girl,name='share_meng_girl'),
    #解鎖
    path('unlock_article',mm.unlock_article,name='unlock_article'),
    #版權聲明
    path('copyright',mm.copyright,name='copyright'),

          
]
