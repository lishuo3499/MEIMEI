from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mm.models import *
import random
from django.contrib.auth import authenticate, login   #用户
from django.contrib.auth.models import User  
from django.contrib.auth import logout  # 注销
from django.contrib.auth.decorators import login_required  #权限控制
from django.db.models import Q
from django.conf import settings
#获取分类

def get_classify2():
    classify2 = Classify.objects.filter( ~Q(classify2 = 0) )
    classify = Classify.objects.filter( classify2 = 0 )
    return {'classify2':classify2,'classify':classify}


def home(request):
    # return render(request,'home.html',)
    return redirect('http://www.ameizi.cn:8008/hot_art')


def copyright(request):
    classify = get_classify2()['classify']
    return render(request,'copyright.html', {'classify':classify})



def hot_art(request):
    wheel = Hot_article.objects.all().order_by('-id')[:15]
    # 查询分类
    classify = get_classify2()['classify']
    classify2 = get_classify2()['classify2']

    article = Hot_article.objects.all().order_by('-id')[:30]

    return render(request,'hot_art.html',
    {'classify':classify,'classify2':classify2,'articles':article,'wheel':wheel}
    )

def index(request):
    wheel = Article.objects.all().order_by('-id')[:15] 
    # 查询分类
    classify = get_classify2()['classify']
    classify2 = get_classify2()['classify2']
    #查询分类文章
    type = request.GET['type']
    this_classify = Classify.objects.filter(classify=type)[0]
    article = this_classify.classify_art.all().order_by('-id')

    paginator = Paginator(article,20)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'index.html',
    {'classify':classify,'classify2':classify2,'articles':contacts,'wheel':wheel})

# 收藏
def collect(request):
    Collect.objects.create(
        article_id=Article.objects.get(id=request.POST['article_id']) ,
        user_id = UserProfile.objects.get(id = request.POST['user_id'])
    )
    response = JsonResponse({"success":'ok'} )
    return response
# 修改封面圖方法
from django.core import serializers
def change_fm(request):
    if request.method == 'POST':
        # print(request.POST['id'])
        article = Article.objects.get(id=request.POST['art_id'])
        article.fm_img = Img.objects.get(id=request.POST['id'])
        article.save()
        return HttpResponse(json.dumps({
            "status":1,
            "result":"sucuss"
        }))
    elif request.method == 'GET':
        # print(request.GET['id'])
        img_data = []
        art_img = Art_img.objects.filter(article_id = request.GET['id'])
        for i in art_img:
            img_data.append(Img.objects.get(id = i.img_id.id))
        data = serializers.serialize("json", img_data)
        return JsonResponse(data, safe=False)
# 發表頁面
import shutil
def send(request):
    return render(request,'send.html',{'classify':get_classify2()['classify'],'classify2':get_classify2()['classify2']})
import time
def upload_img(request):  # 上传文件
    img_list = request.FILES.getlist('img_file')
    randomNum = ''
    for i in img_list:
        t = time.time()
        randomNum = random.randint(0, 9999999)
        i.name = "%s%s.png" % (int(round(t * 1000)),randomNum)
    # 封面图
    fm_img_f = request.FILES.get('fm_img')
    t = time.time()
    randomNum = random.randint(0, 9999999)
    fm_img_f.name = "%s%s.png" % (int(round(t * 1000)),randomNum)
    fm_img_up =  Img(
        img_file = request.FILES.get('fm_img')
    )
    fm_img_up.save()
    # 文章
      
    classify2_post_m = ''
    if request.POST['classify2']  == '':
        classify2_post_m = None
    else:
        classify2_post_m =Classify.objects.filter(id =request.POST['classify2'])[0]

    article = Article(
        id = Article.objects.last().id + 1,
        user_id = request.user.id,
        title = request.POST['title'],
        text = request.POST['text'],
        classify =Classify.objects.filter(id =request.POST['classify'])[0],
        classify2 = classify2_post_m,
        fm_img = fm_img_up
    )
    article.save()
    # 图片
    for img in img_list:
        new_img = Img(
            img_file = img
            )
        new_img.save()
        Art_img.objects.create(
            article_id = article,
            img_id = new_img
        )  
    path_a = r'C:\\Users\\Administrator\\Desktop\\MEIMEI\\mei\\static\\up_load\\img'
    path_b = r'C:\\phpStudy\\PHPTutorial\\WWW\\static\\up_load\\img'
    dirs = os.listdir( path_a )
    for dirname in dirs:
        shutil.move('C:\\Users\\Administrator\\Desktop\\MEIMEI\\mei\\static\\up_load\\img\\'+dirname,
            'C:\\phpStudy\\PHPTutorial\\WWW\\static\\up_load\\img')
    return redirect('/hot_art')



def single(request):
    lock_or = False
    classify = Classify.objects.filter( classify2 = 0 )
    this_page = request.GET['page']
    # 判断是否收藏
    collection_or = 0
    if request.user.is_authenticated:
        this_collect_or = Collect.objects.filter(user_id = request.user.id,article_id=this_page)
        if len(this_collect_or)>0:
            collection_or = 1
    else:
        print('xxxx')
    # 上一页下一页判断
    this1 = int(this_page)+1
    this2 = int(this_page)-1
    # 上一页下一页判断
    if this2 < Article.objects.first().id:
        print('===')
        this2 = Article.objects.first().id
    else:
        print('---')
        this2 = Article.objects.filter(id__lt=this_page).all().order_by("id").last().id

    if this1>Article.objects.last().id:
        this1 = Article.objects.last().id
    else:
        this1 = Article.objects.filter(id__gt=this_page).all().order_by("id").first().id 

    #存储点击量    
    article = Article.objects.filter(id =this_page )[0]
    article.visit_num = article.visit_num+1 #存储点击量
    article.save() 
    # 查询当前图集的图片
    this_user_lock = Lock_article.objects.filter(article_id=article.id,user_id = request.user.id)
    if len(this_user_lock) > 0:
        lock_or = True
        art_img = Art_img.objects.filter(article_id=article.id) #查询图片
    else:
        art_img = []
    return render(request,'single.html',{'lock_or':lock_or,'collection_or':collection_or,'article':article,'art_img':art_img,'classify':classify,'this1':this1,'this2':this2})
    

# 用户系统用户系统用户系统

def loginPage(request):
	return render(request,'login.html')

#登陆验证
def loginValidation(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect('/hot_art')
    else:
        return redirect('login')
        
#注销
def logoutPage(request):
    logout(request)
    return redirect('/hot_art')


# 注册
from django.contrib.auth.models import User
def registration(request):
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = UserProfile.objects.create_user(username=username, email=email, password=password)
    return redirect('login')





# 后台管理
# 我的收藏
def attention(request):
    my_collect = Collect.objects.filter(user_id=request.user.id)
    return render(request,'admin/attention.html',{'my_collect':my_collect})

def m_classify(request):
    return render(request,'admin/classify_manage.html',{'classify':get_classify2()['classify'],'classify2':get_classify2()['classify2']})
# 個人中心
def my_info(request):
    user_info = UserProfile.objects.get(id = request.user.id)
    my_art = Article.objects.filter( user_id = request.user.id )
    article = Article.objects.all().order_by('-id')[:10]
    return render(request,'admin/my_info.html'
    ,{'user_info':user_info,
    'my_art_num':len(my_art),
    'my_art':article
    }
    )

#分享链接
def share_meng_girl(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]
    else:
        client_ip = request.META['REMOTE_ADDR']
    print(client_ip)
    user_id = request.GET['user_id']

    user_share = User_share.objects.filter(user_id=user_id,target_u_ip=client_ip)
    if len(user_share)>0:
        return redirect('/home')
    else:
        User_share.objects.create(user_id= UserProfile.objects.get(id = user_id),target_u_ip=client_ip)
        user_info = UserProfile.objects.get(id = user_id)
        user_info.jb_num = user_info.jb_num + 2
        user_info.save()
        return redirect('/home')

# 解鎖套圖
def unlock_article(request):
    article_id = request.POST['article_id']
    user_info = UserProfile.objects.get(id = request.user.id)
    if user_info.jb_num > 0:
        Lock_article.objects.create(
            article_id = Article.objects.get(id = article_id),
            user_id = user_info
             )
        user_info.jb_num = user_info.jb_num - 1
        user_info.save()
        response = JsonResponse({"success":1})
        return response
    else:
        response = JsonResponse({"success":0})
        return response


# 我的上傳
def my_article(request):
    my_art = Article.objects.filter(user_id=request.user.id).order_by('-id')
    paginator = Paginator(my_art,50)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'admin/my_article.html',{'my_art':contacts})


#添加二級分類
def add_classify2(request):
    c_name = request.POST['c_name']
    f_id = request.POST['classify1']
    # print(request.POST)
    Classify.objects.create(
        title = c_name,
        classify2 = Classify.objects.get(id = f_id)
    )
    return redirect('m_classify')


from django.http import JsonResponse



def delete_c(request):
    Classify.objects.get( id = request.POST['id'] ).delete()
    response = JsonResponse({"success":'ok'} )
    return response
# 取消收集
def delete_collect(request):
    Collect.objects.get( id = request.POST['id'] ).delete()
    response = JsonResponse({"success":'ok'} )
    return response

# 刪除我的上傳
def delete_myart(request):
    Article.objects.get( id = request.POST['id'] ).delete()
    response = JsonResponse({"success":'ok'} )
    return response




# 熱門管理
def hot_manage(request):
    hot = Hot_article.objects.all().order_by('-id')[:30]
    my_art = Article.objects.filter(user_id=request.user.id).order_by('-id')
    paginator = Paginator(my_art,50)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,'admin/hot_manage.html',{'my_art':contacts,'hot':hot})


# 設置熱門
def set_hot(request):
    type = request.POST['type']
    id = request.POST['id']
    if type == '0':  #設置
        print('----')
        Hot_article.objects.create(article_id = Article.objects.get(id=id))
    else:            #刪除
        print('====')
        Hot_article.objects.get(id = id).delete()
    # Article.objects.get( id = request.POST['id'] ).delete()
    response = JsonResponse({"success":'ok'} )
    return response



# 上傳
import json
import os
def admin_upload_s(request):
    path = r'C:\\Users\\lishuo\\Downloads\\NeoDownloader\\m131-Xinggan\\img1.mm131.me\\pic'
    dirs = os.listdir( path )
    # dirs.sort(key=lambda x:int(x[:-1]))
    qikan = 1
    for dirname in dirs:
        filename = os.listdir( path+'\\'+dirname )
        fm_img_up =  Img(   #封面图
            img_file ='mm131/xinggan/'+dirname+'/'+filename[0]
            )
        fm_img_up.save()
        article = Article(
            user_id = request.user.id,
            title = '第'+ str(qikan)+'期',
            text = '',
            classify =Classify.objects.filter(id = 6)[0],
            classify2 = None,
            fm_img = fm_img_up
        )
        article.save()
        # print(qikan)
        qikan = qikan +1
        # print('第'+ str(qikan)+'期创建成功')
        for i in filename:
            new_img = Img(
                img_file = 'mm131/xinggan/'+dirname+'/'+i
                )
            new_img.save()
            Art_img.objects.create(
                article_id = article,
                img_id = new_img
            ) 
    # return render(request,'admin/admin_upload_s.html')
    return HttpResponse('ok')

# 隨機匹配
import random
def random_img(request):
    classify = get_classify2()['classify']
    all = []
    first_id = Img.objects.first().id
    last_id =  Img.objects.last().id
    for i in range(1,15):
        random_num = random.randint(first_id,last_id)
        image = Img.objects.get(id=random_num)
        # print(image.img_file)
        all.append('http://114.116.165.218/static/'+str(image.img_file))
    # print(all)
    return render(request,"randomImg.html",
        {'classify':classify,
        "all":all}
        )

   

        


    









