import random,string,uuid,os
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
import MySQLdb
from admins.models import Admins
from captcha.image import ImageCaptcha
# Create your views here.

# 创建唯一的文件名
def generateUUID(filename):
    id = str(uuid.uuid4())
    extend = os.path.splitext(filename)[1]
    return id + extend
# 主页
def index(request):
    print('This is index page')
    username = request.session.get('username')
    headpic = request.COOKIES.get('headpic')
    if username:
        return render(request, 'index.html', {'username': username,'headpic':headpic})
    return render(request, 'index.html')

#注册页面
def register(request):
    print('This is registeer page')
    return render(request,'regist.html')

#注册逻辑处理，读取用户注册信息，连接数据库保存用户数据
def regist_logic(request):
    print('This is regist_logic,save user data and goto login')
    username = request.POST.get('username')
    realname = request.POST.get('realname')
    passwd = request.POST.get('pwd')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    birth = request.POST.get('birth')
    hpic = request.FILES.get('hpic')
    hpic.name = generateUUID(hpic.name)  # 调用自定义的generateUUID生成唯一文件名
    data = Admins.objects.filter(username=username)
    print('data',data)
    try:
        with transaction.atomic():
            if data:
                return HttpResponse('对不起，该用户名已被注册！请返回重新注册！')
            else:
                addadmin = Admins(username=username,realname=realname, age=age, gender=gender, birth=birth, passwd=passwd,hpic=hpic)
                addadmin.save()
                return HttpResponse('{"result":1,"path":"' + addadmin.hpic.url + '"}')
    except:
        return HttpResponse('{"result":0}')
# #登录请求
def login(request):
    print('This is going to login page')
    res = render(request, 'login.html')
    username = request.COOKIES.get('username')
    if username:
        return render(request, 'login.html',{'username':username})
    return res

#登录逻辑处理：核对用户提交的登录信息，并作出响应信息
def login_logic(request):
    print('This is login_logic')
    username = request.POST.get('name')
    passwd = request.POST.get('pwd')
    user = Admins.objects.get(username=username)
    try:
        with transaction.atomic():
            datauser = Admins.objects.filter(username=username)[0]
            rem = request.POST.get('rem')
            res = HttpResponse('1')
            #如果登录成功(datauser为True)：再判断是否勾选记住我
            if datauser.passwd== passwd :
                #若登录成功创建session，标记登录状态的login和已登录的用户名称
                request.session['login']=1
                request.session['username']=username
                res.set_cookie('headpic',user.hpic.url,60*60*24*3)
                #如果勾选记住我则创建cookie,并随响应传递到客户端浏览器
                if rem:
                    res.set_cookie('username',username,60*60*24*7)
                return res
            return HttpResponse('0')
    except:
        return HttpResponse('登录失败，请重试！')


#生成验证码
def getCode(request):
    #创建一个Image对象
    myImg = ImageCaptcha()
    #创建一个随机码，默认列表形式，并转换为字符串
    code = random.sample(string.ascii_letters+string.digits,4)
    code = ''.join(code)
    print(code)
    #设置session以备在其他页面中获取并验证
    request.session['code'] = code
    data = myImg.generate(code)
    return HttpResponse(data,'image/png')

#异步验证验证码
def checkCode(request):
    mycode = request.GET.get('mycode')
    session_code = request.session.get('code')
    print('getsission:',session_code,'mycode:',mycode)
    if session_code.lower() == mycode.lower():
        return HttpResponse('1')
    return HttpResponse('0')

#验证用户名是否存在
def checkName(request):
    names = request.GET.get('name')
    print('names:', names)
    isname = Admins.objects.filter(username=names)
    if isname:
        return HttpResponse('0')
    return HttpResponse('1')


