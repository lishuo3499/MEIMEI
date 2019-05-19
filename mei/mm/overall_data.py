# def staticAddress(request):
#     static_address = 'www.linke.xtu.edu.cn'
#     return {'static_address':static_address}
def global_setting(request):   
    content = {
        'STATIC_URL': 'http://www.ameizi.cn:8009',   #把setting定义的读取出来
        # 'STATIC_URL': 'http://linke.xtu.edu.cn',   #把setting定义的读取出来
    }
    return content