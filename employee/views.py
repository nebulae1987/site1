from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from employee.models import Emplist
from django.db import transaction
import traceback

# Create your views here.

#查询所有员工：
def query_all(request):
    print('This is query all page')
    login = request.session.get('login')
    username = request.session.get('username')
    num = request.GET.get('num')
    if not num:
        num = request.session.get('p_number')
        if num:
            del request.session['p_number']
        if not num:
            num = 1
    num = int(num)
    #所有搜索提交的用户名则返回该用户列表，否则返回全部用户列表
    empname = request.GET.get('empname')
    sec_emp = Emplist.objects.all()
    if empname:
        sec_emp = Emplist.objects.filter(name=empname)
    pagtor = Paginator(sec_emp,per_page=4)
    headpic = request.COOKIES.get('headpic')
    if pagtor.num_pages>=num:
        page = pagtor.page(num)
    else:
        page = pagtor.page(num-1)
    if not login:
        return redirect('adm:ad:log')
    return render(request,'employee/emplist.html',{'username':username,'page':page,'headpic':headpic})

#员工管理：添加员工
def addEmp(request):
    print('This is add employee')
    return render(request,'employee/addEmp.html')

def add_Emp(request):
    print('This is add employee')
    name = request.POST.get('name')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    birth   = request.POST.get('birth')
    salary = request.POST.get('salary')
    hpic = request.FILES.get('hpic')
    try:
        with transaction.atomic():
            addemp = Emplist(name = name,age = age,gender = gender,birth = birth,salary = salary,hpic=hpic)
            addemp.save()
            return HttpResponse('{"result":"1","path":"'+addemp.hpic.url+'"}')
    except:
        return HttpResponse('{"result":"0"}')
#员工管理：删除员工
def delEmp(request):
    print('this is delete employee')
    id = request.GET.get('id')
    p_num = request.GET.get('num')
    #创建要删除员工所在页面的session
    request.session['p_number']=p_num
    Emplist.objects.get(id=id).delete()
    return redirect('emp:query')

#员工管理：修改员工信息
def updateEmp(request):
    print('this is update employee')
    id = request.GET.get('id')
    emp = Emplist.objects.get(id=id)
    return render(request, 'employee/updateEmp.html',{'emp' : emp})

def update_Emp(request):
    print('this is update employee')
    id = request.POST.get('id')
    name = request.POST.get('name')
    age = request.POST.get('age')
    birth  = request.POST.get('birth')
    gender = request.POST.get('gender')
    salary = request.POST.get('salary')
    hpic = request.FILES.get('hpic')
    try:
        with transaction.atomic():
            user = Emplist.objects.get(id = id)
            user.name = name
            user.age = age
            user.birth = birth
            user.gender = gender
            user.salary = salary
            user.hpic = hpic
            user.save()
            return redirect('emp:query')
    except:
        print("update employee error")
        traceback.print_exc()             # 打印异常栈信息

#搜索员工
def sec(request):
    print('this is seach employee')
    username = request.POST.get('name')
    sug = list(Emplist.objects.filter(name__icontains=username).values())
    print(sug)
    return JsonResponse(sug,safe=False)



