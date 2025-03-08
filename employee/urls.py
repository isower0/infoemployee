from django.urls import path
from .views import register_view, login_view, logout_view,employee_list_view,add_employee_view,employee_detail

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('employees/', employee_list_view, name='employee_list'),
    path('employees/<int:emp_id>/', employee_detail, name='employee_detail'),  # หน้า Detail
    path('employees/add/', add_employee_view, name='add_employee'),  # เพิ่ม URL สำหรับเพิ่มพนักงาน
]