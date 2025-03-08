from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .forms import EmployeeForm
from django.db.models import Q  # ใช้ Q object เพื่อค้นหาหลายฟิลด์
from django.core.paginator import Paginator
import base64

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.username})
    else:
        return redirect('employee/login.html')  # ถ้ายังไม่ล็อกอินให้ไปหน้า login
    
def add_employee_view(request):
    if request.method == 'POST':
        # print("Request FILES:", request.FILES)  # Debug เช็ค request.FILES
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            # แปลงรูปภาพเป็น Base64
            # เช็คว่าได้รับไฟล์รูปไหม
            image_file = request.FILES.get('image')
            # print("Image File:", image_file)  # Debug ดูว่ามีไฟล์ไหม

            if image_file:
                image_data = image_file.read()  # อ่านไฟล์
                image_base64 = base64.b64encode(image_data).decode('utf-8')  # แปลงเป็น Base64
                # print("Base64 Data:", image_base64[:50])  # Debug ดูค่าที่ได้ (เอาแค่ 50 ตัวแรก)
                employee.image_base64 = image_base64  # เก็บลง Model

            employee.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return redirect('employee_list')  # เปลี่ยนเส้นทางไปยังหน้าแสดงรายชื่อพนักงาน
    else:
        form = EmployeeForm()  # หากเป็น GET ให้แสดงฟอร์มเปล่า
    
    return render(request, 'employee/add_employee.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'employee/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'employee/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from .models import Employee


def employee_list_view(request):
    query = request.GET.get('search_emp','')
    page_number = request.GET.get('page', 1)  # รับค่าหมายเลขหน้าจาก URL
    employees = Employee.objects.all()
    # ค้นหาข้อมูล (ถ้ามี query)
    if query:
        employees = employees.filter(
             Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)|
            Q(phone_number__icontains=query) |
            Q(department__icontains=query) 
        )

    # ใช้ Paginator แบ่งหน้าละ 10 รายการ
    paginator = Paginator(employees, 10)  
    page_obj = paginator.get_page(page_number)
    return render(request, 'employee/employee_list.html', {'page_obj': page_obj, 'query': query})

def employee_detail(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)  # ดึงข้อมูลพนักงานจาก ID
    # print(employee)
    return render(request, 'employee/employee_detail.html', {'employee': employee})