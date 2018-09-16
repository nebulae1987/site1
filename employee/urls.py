from django.urls import path, include
from employee import views


urlpatterns = [
    path('query/',views.query_all,name='query'),
    path('emps/', include(([
                        path('addemp/', views.addEmp,name='add'),
                        path('add_emp/', views.add_Emp,name='addc'),
                        path('delemp/', views.delEmp,name='del'),
                        path('updateemp/', views.updateEmp,name='up'),
                        path('updat_emp/', views.update_Emp,name='upc'),
                        #搜索员工
                        path('sec/', views.sec,name='sec'),


                    ],'em'))),

]