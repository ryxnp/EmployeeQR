from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse
import requests

from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime

def context_data():
    context = {
        'page_name' : '',
        'page_title' : 'Chat Room',
        'system_name' : 'Employee Logs',
        'topbar' : True,
        'footer' : True,
    }

    return context


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['employees'] = models.Employee.objects.count()
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def employee_list(request):
    context = context_data()
    context['page'] = 'employee_list'
    context['page_title'] = 'Employee List'
    
    # Fetch all employees
    employee_list = models.Employee.objects.all()
    
    # Set up pagination
    paginator = Paginator(employee_list, 10)  # Show 10 employees per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the request
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # If page is not an integer, deliver first page
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page

    context['employees'] = page_obj  # Update context to include paginated employees
    context['total_employees'] = paginator.count  # Total number of employees

    return render(request, 'employee_list.html', context)

@login_required
def base_scanner(request):
    context =context_data()
    context['page'] = 'base_scanner'
    context['page_title'] = 'Scan Code Here'
    context['employees'] = models.Employee.objects.all()

    return render(request, 'base_scanner.html', context)

@login_required 
def manage_employee(request, pk=None):
    context =context_data()
    if pk is None:
        context['page'] = 'add_employee'
        context['page_title'] = 'Add New Employee'
        context['employee'] = {}
    else:
        context['page'] = 'edit_employee'
        context['page_title'] = 'Update Employee'
        context['employee'] = models.Employee.objects.get(id=pk)

    return render(request, 'manage_employee.html', context)

@login_required
def save_employee(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent into the request."

    else:
        if request.POST['id'] == '':
            form = forms.SaveEmployee(request.POST, request.FILES)
        else:
            employee = models.Employee.objects.get(id = request.POST['id'])
            form = forms.SaveEmployee(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                messages.success(request, f"{request.POST['employee_code']} has been added successfully.")
            else:
                messages.success(request, f"{request.POST['employee_code']} has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")
                    resp['msg'] += str(f"[{field.label}] {error}")

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Employee ID is Invalid")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(id=pk)
        return render(request, 'view_id.html', context)

@login_required
def view_scanner(request):
    context = context_data()
    return render(request, 'scanner.html', context)


@login_required
def view_details(request, code = None):
    if code is None:
        return HttpResponse("Employee code is Invalid")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(employee_code=code)
        return render(request, 'view_details.html', context)

@login_required
def delete_employee(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No data has been sent into the request."
    else:
        try:
            models.Employee.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Employee has been deleted successfully.')
        except:
            resp['msg'] = "Employee has failed to delete."

    return HttpResponse(json.dumps(resp), content_type="application/json")

# @login_required
# def view_record(request, pk=None):
#     if pk is None:
#         return HttpResponse("Employee code is Invalid")
#     else:
#         context = context_data()
#         # Use get_object_or_404 to handle missing records
#         context['logrecord'] = get_object_or_404(models.LogRecord, employee_pk=pk)
#         return render(request, 'view_record.html', context)

# @login_required
# def view_record(request, pk = None):
#     if pk is None:
#         return HttpResponse("Employee code is Invalid")
#     else:
#         context = context_data()
#         context['employee'] = models.Employee.objects.get(id=pk)
#         return render(request, 'view_record.html', context)

@login_required
def view_record(request, pk=None):
    if pk is None:
        return JsonResponse({"error": "Employee code is Invalid"}, status=400)

    # Define the API endpoints
    employee_api_url = f"http://127.0.0.1:8000/api/employee/{pk}/"
    logrecord_api_url = f"http://127.0.0.1:8000/api/logrecord/?employee_id={pk}"

    try:
        # Fetch employee details
        employee_response = requests.get(employee_api_url)
        employee_response.raise_for_status()  # Raise an error for bad responses
        employee_data = employee_response.json()

        # Fetch log records for the specific employee
        logrecord_response = requests.get(logrecord_api_url)
        logrecord_response.raise_for_status()
        logrecords_data = logrecord_response.json()

        # Filter log records by employee_pk (if needed)
        filtered_logrecords = [
            record for record in logrecords_data if record.get('employee_pk') == pk
        ]

        # Format dates and times for each log record
        for record in filtered_logrecords:
            record['date_created'] = format_datetime(record.get('date_created'))
            record['time'] = format_datetime(record.get('time'))

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Prepare context data for rendering
    context = {
        'employee': employee_data,
        'logrecords': filtered_logrecords,  # Use the filtered records
    }

    return render(request, 'view_record.html', context)

def format_datetime(datetime_str):
    """Convert a datetime string to a formatted string."""
    if datetime_str:
        dt = parse_datetime(datetime_str)  # Parse the datetime string
        if dt:
            local_dt = localtime(dt)  # Convert to local time
            return local_dt.strftime("%B %d, %Y %I:%M %p")  # Format as desired (e.g., October 10, 2024 10:36 AM)
    return ""