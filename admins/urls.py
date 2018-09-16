from django.contrib import admin
from django.urls import path, include
from admins import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #管理员的注册和登录路径
    path('admins/',include(([
                            path('regist/',views.register,name='reg'),
                            path('regist_logic/',views.regist_logic,name='regc'),
                            path('login/',views.login,name='log'),
                            path('login_logic/',views.login_logic,name='logc'),
                            #获取验证码逻辑
                            path('getCode/',views.getCode,name='getCode'),
                            #验证用户输入验证码逻辑
                            path('checkCode/',views.checkCode,name='checkCode'),
                            #验证用户名是否已经存在
                            path('checkName/',views.checkName,name='checkName'),




                             ],'ad'))),

]