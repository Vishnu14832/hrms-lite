from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def add_employee(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        full_name = request.POST['full_name']
        email = request.POST['email']
        department = request.POST['department']

        if Employee.objects.filter(employee_id=employee_id).exists():
            messages.error(request, "Employee ID already exists")
        else:
            Employee.objects.create(
                employee_id=employee_id,
                full_name=full_name,
                email=email,
                department=department
            )
            return redirect('employee_list')

    return render(request, 'add_employee.html')

def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee_list')


from django.db import IntegrityError

def mark_attendance(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        employee_id = request.POST['employee']
        date = request.POST['date']
        status = request.POST['status']

        employee = Employee.objects.get(id=employee_id)

        try:
            Attendance.objects.create(
                employee=employee,
                date=date,
                status=status
            )
            messages.success(request, "Attendance Marked Successfully")
            return redirect('attendance_list')

        except IntegrityError:
            messages.error(request, "Attendance already marked for this date")

    return render(request, 'mark_attendance.html', {'employees': employees})



def attendance_list(request):
    records = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'records': records})
