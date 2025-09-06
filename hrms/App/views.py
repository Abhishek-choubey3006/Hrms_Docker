from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Attendance, Payroll, Projects, LeaveRequest, Notifications, Meeting, Job, Task

from .utils import log_activity

from .forms import *
from .models import *
from datetime import date

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                messages.success(request, "Admin login successful")
                return redirect('admin_page')
            elif user.is_staff:
                if Employee.objects.filter(user=user).exists():
                    messages.success(request, "Employee login successful")
                    return redirect('employee_page')
                else:
                    messages.info(request, 'Please complete your employee profile.')
                    return render(request, 'signup2.html')
            else:
                messages.error(request, "No role assigned to this user.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'loginpage2.html')

# ----- Signup View -----
def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User already exists, please login.')
            return redirect('user_login')

        new_user = User.objects.create_user(username=username, email=email, password=password)

        if role == "admin":
            new_user.is_superuser = True
            new_user.is_staff = True
        elif role == "employee":
            new_user.is_staff = True

        new_user.save()

        if role == "employee":
            Employee.objects.create(user=new_user, hire_date=date.today(), email=email)

        messages.success(request, "User registered successfully.")
        return redirect('user_login')

    return render(request, "signup2.html")

# ----- Logout View -----
def user_logout(request):
    auth_logout(request)
    return redirect('user_login')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
import plotly.express as px
from .models import Employee, Attendance, Payroll, Projects, LeaveRequest, Notifications, Meeting, MySkill, Task


@login_required
def EmployPage(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect("user_login")

    # ---------------- ATTENDANCE TREND ----------------
    attendance_data = Attendance.objects.filter(user=employee).values(
        "date", "punch_in_time", "punch_out_time", "production_hours"
    )
    attendance_df = pd.DataFrame(attendance_data)

    if not attendance_df.empty:
        attendance_df["date"] = pd.to_datetime(attendance_df["date"])
        attendance_chart = px.line(
            attendance_df,
            x="date",
            y="production_hours",
            title="Daily Attendance & Working Hours",
            markers=True,
        )
        attendance_chart_html = attendance_chart.to_html(full_html=False)
    else:
        attendance_chart_html = "<p>No attendance data available</p>"

    # ---------------- LEAVE REQUEST STATUS ----------------
    leave_data = LeaveRequest.objects.filter(employee=request.user).values("status")
    leave_df = pd.DataFrame(leave_data)
    if not leave_df.empty:
        leave_chart = px.pie(
            leave_df,
            names="status",
            title="Leave Request Status",
        )
        leave_chart_html = leave_chart.to_html(full_html=False)
    else:
        leave_chart_html = "<p>No leave request data available</p>"

    # ---------------- PAYROLL SUMMARY ----------------
    payroll_data = Payroll.objects.filter(employee=request.user).values("month", "net_salary")
    payroll_df = pd.DataFrame(payroll_data)
    if not payroll_df.empty:
        payroll_df["month"] = pd.Categorical(
            payroll_df["month"],
            categories=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            ordered=True,
        )
        payroll_df = payroll_df.sort_values("month")
        payroll_chart = px.bar(
            payroll_df,
            x="month",
            y="net_salary",
            color="month",
            title="Salary Summary",
        )
        payroll_chart_html = payroll_chart.to_html(full_html=False)
    else:
        payroll_chart_html = "<p>No payroll data available</p>"

    # ---------------- SKILL PERFORMANCE ----------------
    skill_data = MySkill.objects.filter(employee=employee).values("skill", "percentage")
    skill_df = pd.DataFrame(skill_data)
    if not skill_df.empty:
        skill_chart = px.bar(
            skill_df,
            x="skill",
            y="percentage",
            color="skill",
            title="Skill Performance (%)",
        )
        skill_chart_html = skill_chart.to_html(full_html=False)
    else:
        skill_chart_html = "<p>No skill data available</p>"

    # ---------------- UPCOMING MEETINGS ----------------
    meetings = Meeting.objects.filter(participants=employee).order_by("date_meeting")[:5]

    # ---------------- ASSIGNED PROJECTS ----------------
    projects = Projects.objects.filter(user=request.user)

    # ---------------- TASKS ----------------
    tasks = Task.objects.filter(assigned_to=request.user)

    # ---------------- LATEST NOTIFICATIONS ----------------
    notifications = Notifications.objects.filter(recipients=request.user).order_by("-created_at")[:5]

    # ---------------- CONTEXT ----------------
    context = {
        "Employee": employee,
        "Attendance": Attendance.objects.filter(user=employee),
        "MySkill": MySkill.objects.filter(employee=employee),
        "projects": projects,
        "tasks": tasks,
        "meetings": meetings,
        "notifications": notifications,
        "is_admin": False,
        "is_employee": True,
        "attendance_chart": attendance_chart_html,
        "leave_chart": leave_chart_html,
        "payroll_chart": payroll_chart_html,
        "skill_chart": skill_chart_html,
    }

    return render(request, "Employee/EmployPage.html", context)




@login_required
def AdminPage(request):
    # ---------------- ATTENDANCE CHART ----------------
    attendance_data = Attendance.objects.all().values("punch_in_time", "punch_out_time")
    attendance_df = pd.DataFrame(attendance_data)

    if not attendance_df.empty:
        attendance_df["Status"] = attendance_df["punch_in_time"].apply(
            lambda x: "Present" if pd.notnull(x) else "Absent"
        )
        attendance_chart = px.pie(
            attendance_df,
            names="Status",
            title="Attendance Overview"
        )
        attendance_chart_html = attendance_chart.to_html(full_html=False)
    else:
        attendance_chart_html = "<p>No attendance data available</p>"

    # ---------------- EMPLOYEE STATUS ----------------
    employee_data = Employee.objects.values("status")
    employee_df = pd.DataFrame(employee_data)

    if not employee_df.empty:
        employee_chart = px.pie(
            employee_df,
            names="status",
            title="Employee Status"
        )
        employee_chart_html = employee_chart.to_html(full_html=False)
    else:
        employee_chart_html = "<p>No employee data available</p>"

    # ---------------- DEPARTMENT DISTRIBUTION ----------------
    dept_df = pd.DataFrame(Employee.objects.values("department"))
    if not dept_df.empty:
        dept_df = dept_df["department"].value_counts().reset_index()
        dept_df.columns = ["Department", "Count"]
        dept_chart = px.bar(
            dept_df,
            x="Department",
            y="Count",
            color="Count",
            title="Employees by Department"
        )
        dept_chart_html = dept_chart.to_html(full_html=False)
    else:
        dept_chart_html = "<p>No department data available</p>"

    # ---------------- PAYROLL EXPENSES ----------------
    payroll_df = pd.DataFrame(Payroll.objects.values("month", "net_salary"))
    if not payroll_df.empty:
        payroll_df["month"] = pd.Categorical(
            payroll_df["month"],
            categories=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            ordered=True
        )
        payroll_df = payroll_df.sort_values("month")
        payroll_chart = px.bar(
            payroll_df,
            x="month",
            y="net_salary",
            color="month",
            title="Monthly Payroll Expenses"
        )
        payroll_chart_html = payroll_chart.to_html(full_html=False)
    else:
        payroll_chart_html = "<p>No payroll data available</p>"

    # ---------------- PROJECT PRIORITY ----------------
    project_df = pd.DataFrame(Projects.objects.values("priority"))
    if not project_df.empty:
        project_df = project_df["priority"].value_counts().reset_index()
        project_df.columns = ["Priority", "Count"]
        project_chart = px.bar(
            project_df,
            x="Priority",
            y="Count",
            color="Priority",
            title="Projects by Priority"
        )
        project_chart_html = project_chart.to_html(full_html=False)
    else:
        project_chart_html = "<p>No project data available</p>"

    # ---------------- LEAVE REQUESTS ----------------
    leave_df = pd.DataFrame(LeaveRequest.objects.values("status"))
    if not leave_df.empty:
        leave_chart = px.pie(
            leave_df,
            names="status",
            title="Leave Request Status"
        )
        leave_chart_html = leave_chart.to_html(full_html=False)
    else:
        leave_chart_html = "<p>No leave data available</p>"

    # ---------------- NEW HIRES (Fixed & Ordered) ✅ ----------------
    hire_df = pd.DataFrame(Employee.objects.values("hire_date"))
    if not hire_df.empty:
        hire_df["hire_date"] = pd.to_datetime(hire_df["hire_date"])
        hire_df["Month"] = hire_df["hire_date"].dt.strftime("%B")

        # Ensure correct month order
        hire_df["Month"] = pd.Categorical(
            hire_df["Month"],
            categories=[
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],
            ordered=True
        )

        hires_per_month = hire_df.groupby("Month", as_index=False)["hire_date"].count()
        hires_per_month.rename(columns={"hire_date": "New Hires"}, inplace=True)

        hires_chart = px.line(
            hires_per_month,
            x="Month",
            y="New Hires",
            title="New Hires Trend",
            markers=True
        )
        hires_chart_html = hires_chart.to_html(full_html=False)
    else:
        hires_chart_html = "<p>No hiring data available</p>"

    # ---------------- TOP PERFORMERS ----------------
    top_df = pd.DataFrame(Employee.objects.values("first_name", "last_name", "performance_score"))
    if not top_df.empty:
        top_df = top_df.sort_values(by="performance_score", ascending=False).head(5)
        top_df["Employee"] = top_df["first_name"] + " " + top_df["last_name"]
        top_chart = px.bar(
            top_df,
            x="Employee",
            y="performance_score",
            color="Employee",
            title="Top Performers"
        )
        top_chart_html = top_chart.to_html(full_html=False)
    else:
        top_chart_html = "<p>No performance data available</p>"

    # ---------------- CONTEXT DATA ----------------
    context = {
        'Employee': Employee.objects.all(),
        'payroll': Payroll.objects.all(),
        'attendence': Attendance.objects.all(),
        "All_Notifications": Notifications.objects.all().order_by('-created_at')[:5],
        'Meeting': Meeting.objects.all(),
        'is_admin': True,
        'is_employee': False,
        'Project': Projects.objects.all(),
        'Job': Job.objects.all(),
        'tasks': Task.objects.all(),
        "attendance_chart": attendance_chart_html,
        "employee_chart": employee_chart_html,
        "dept_chart": dept_chart_html,
        "payroll_chart": payroll_chart_html,
        "project_chart": project_chart_html,
        "leave_chart": leave_chart_html,
        "hires_chart": hires_chart_html,
        "top_chart": top_chart_html,
    }

    return render(request, "Admin/AdminPage.html", context)


# Employee All details
@login_required
def employee_Notification(request):
    user = request.user
    notifications = Notifications.objects.filter(recipients=user).order_by('-created_at')

    return render(request, 'Employee/notificaion.html', {'notifications': notifications})
# Apply Leave
@login_required
def apply_leave_view(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.target = 'Admin'
            leave.save()
            messages.success(request, "Leave request submitted successfully!")
            return redirect('leave_status')
    else:
        form = LeaveRequestForm()

    return render(request, 'Employee/Apply_Leave.html', {'form': form})

# Leave Status
@login_required
def leave_status_view(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'Employee/Leave_Status.html', {'leaves': leaves})

# payroll view
# Employee view: view their own payroll
@login_required
def view_my_payroll(request):
    payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
    return render(request, 'Employee/my_payroll.html', {'payrolls': payrolls})

# Punch In/Out View
@login_required
def punch_in(request):
    today = timezone.localdate()
    now = timezone.localtime(timezone.now())

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('punch_dashboard')
    if Attendance.objects.filter(user=employee, date=today).exists():
        return redirect('punch_dashboard')

    Attendance.objects.create(
        user=employee,
        punch_in_time=now.time()
    )

    return redirect('punch_dashboard')


@login_required
def punch_out(request):
    now = timezone.localtime(timezone.now())  # ✅ Use local time
    today = now.date()

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('punch_dashboard')
    record = Attendance.objects.filter(user=employee, date=today).order_by('-id').first()

    if record and not record.punch_out_time:
        record.punch_out_time = now.time()

        in_datetime = timezone.make_aware(datetime.combine(record.date, record.punch_in_time))
        out_datetime = now

        record.production_hours = round((out_datetime - in_datetime).total_seconds() / 3600, 2)
        record.save()

    return redirect('punch_dashboard')
@login_required
def punch_dashboard(request):
    today = timezone.localdate()

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return render(request, 'employee/punch_dashboard.html', {
            'error': "No employee profile linked with this user."
        })
    attendance = Attendance.objects.filter(user=employee, date=today).first()

    return render(request, 'Employee/punch.html', {
        'attendance': attendance,
        'employee': employee
    })




# Edit Profile
@login_required
def edit_profile(request):
    log_activity(request.user, "Employee Update profile")
    employee, created = Employee.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_page')
    else:
        form = EmployeeForm(instance=employee)
    

    
    return render(request, 'Employee/Profile.html', {'form': form})



@login_required
def all_events(request):
    events = Event.objects.all()
    event_list = []

    for e in events:
        event_list.append({
            "title": e.title,
            "start": e.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": e.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "description": e.description,
        })

    return JsonResponse(event_list, safe=False)

@login_required
def add_event(request):
    if not request.user.is_staff:
        return redirect('calendar')  # this name must match in urls.py

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('calendar')
    else:
        form = EventForm()

    return render(request, 'Admin/add_event.html', {'form': form})


def test_calendar(request):
    events = Event.objects.all()
    return render(request, 'calendar_test.html', {'events': events})



# Admin View: Manage Leave Requests
@login_required
def admin_leave_requests_view(request):
    if request.method == 'POST':
        try:
            leave_id = request.POST.get('leave_id')
            leave = get_object_or_404(LeaveRequest, id=leave_id)

            leave.status = request.POST.get('status')
            leave.admin_comment = request.POST.get('admin_comment', '')
            # leave.admin_comment = request.POST.get('admin_comment', '')
            leave.is_approved = (leave.status == 'Approved')
            leave.save()

            messages.success(request, "Leave request updated successfully.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
        return redirect('admin_leave_requests')

    leave_requests = LeaveRequest.objects.select_related('employee').all().order_by('-start_date')
    return render(request, 'Admin/admin_leave_requests.html', {
        'leave_requests': leave_requests
    })

@login_required
def manage_payrolls(request):
    # ✅ Fetch ALL users except superuser/admin
    employees = User.objects.filter(is_superuser=False)

    selected_employee_id = request.GET.get('employee_id')
    selected_employee = None
    employee_payrolls = None

    if selected_employee_id:
        selected_employee = get_object_or_404(User, id=selected_employee_id)
        employee_payrolls = Payroll.objects.filter(employee=selected_employee).order_by('-year', '-month')

    if request.method == 'POST':
        payroll_id = request.POST.get('payroll_id')
        if payroll_id:
            payroll = get_object_or_404(Payroll, id=payroll_id)
            form = PayrollForm(request.POST, instance=payroll)
        else:
            form = PayrollForm(request.POST)

        if form.is_valid():
            payroll = form.save(commit=False)
            if not payroll.employee_id:
                payroll.employee_id = selected_employee_id
            payroll.save()
            messages.success(request, 'Payroll saved successfully.')
            return redirect(f'/manage-payrolls/?employee_id={selected_employee_id}')
    else:
        form = PayrollForm()

    return render(request, 'Admin/manage_payrolls.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'employee_payrolls': employee_payrolls,
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def assign_project_view(request):
    if request.method == 'POST':
        form = AssignProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project assigned to {form.cleaned_data['user'].username}")
            messages.success(request, 'Project assigned successfully!')
            return redirect('assign_project')  # or wherever you want to redirect
    else:
        form = AssignProjectForm()

    return render(request, 'Admin/assign_project.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            # for user in form.cleaned_data['assigned_to']:

            #     messages.info(request, f'New task "{task.title}" assigned to {user.username}.')
            #     send_mail(
            #         subject='New Task Assigned',
            #         message=f'Dear {user.username},\n\nYou have been assigned a new task: "{task.title}".\n\nPlease check your dashboard for more details.',
            #         from_email='admin@example.com',
            #         recipient_list=[user.email],
            #         fail_silently=True,
            #     )

            messages.success(request, 'Task created and notifications sent successfully.')
            return redirect('create_task')
    else:
        form = TaskForm()

    return render(request, 'Admin/create_task.html', {'form': form})

def attendance_list(request):
    attendances = Attendance.objects.select_related('user').order_by('-date')
    paginator = Paginator(attendances, 10)  # Show 10 records per page
    # admin_attendance = Attendance.objects.select_related('user').order_by('-date')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Admin/attendance_list.html', {'page_obj': page_obj})


def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message']
            category = form.cleaned_data['category']
            send_to_all = form.cleaned_data.get('send_to_all', True)
            selected_users = form.cleaned_data.get('recipients')
            if send_to_all:
                employees = User.objects.filter(is_staff=True)
            else:
                employees = selected_users
            notification = Notifications.objects.create(
                message=message_text,
                category=category,
            )
            notification.recipients.set(employees)

            # Send email to recipients
            # for employee in employees:
            #     if employee.email:
            #         send_mail(
            #             subject='New Notification from Admin',
            #             message=message_text,
            #             from_email='admin@example.com',
            #             recipient_list=[employee.email],
            #             fail_silently=False
            #         )

            messages.success(request, "Notification sent successfully.")
            return redirect('send_notification')
    else:
        form = NotificationForm()

    return render(request, 'Admin/send_notification.html', {'form': form})



#  chart pandas
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from .models import Attendance, Employee, Payroll, Projects, LeaveRequest

def admin_dashboard(request):
    # ---------------- ATTENDANCE CHART ----------------
    attendance_data = Attendance.objects.all().values("punch_in_time", "punch_out_time")
    attendance_df = pd.DataFrame(attendance_data)

    if not attendance_df.empty:
        attendance_df["Status"] = attendance_df["punch_in_time"].apply(
            lambda x: "Present" if pd.notnull(x) else "Absent"
        )
        attendance_chart = px.pie(attendance_df, names="Status", title="Attendance Overview")
        attendance_chart_html = attendance_chart.to_html(full_html=False)
    else:
        attendance_chart_html = "<p>No attendance data available</p>"

    # ---------------- EMPLOYEE STATUS ----------------
    employee_data = Employee.objects.values("status")
    employee_df = pd.DataFrame(employee_data)

    if not employee_df.empty:
        employee_chart = px.pie(employee_df, names="status", title="Employee Status")
        employee_chart_html = employee_chart.to_html(full_html=False)
    else:
        employee_chart_html = "<p>No employee data available</p>"

    # ---------------- DEPARTMENT DISTRIBUTION ----------------
    dept_df = pd.DataFrame(Employee.objects.values("department"))
    if not dept_df.empty:
        dept_chart = px.bar(dept_df["department"].value_counts().reset_index(),
                            x="index", y="department", color="index",
                            title="Employees by Department")
        dept_chart_html = dept_chart.to_html(full_html=False)
    else:
        dept_chart_html = "<p>No department data available</p>"

    # ---------------- PAYROLL EXPENSES ----------------
    payroll_df = pd.DataFrame(Payroll.objects.values("month", "net_salary"))
    if not payroll_df.empty:
        payroll_chart = px.bar(payroll_df, x="month", y="net_salary", color="month",
                               title="Monthly Payroll Expenses")
        payroll_chart_html = payroll_chart.to_html(full_html=False)
    else:
        payroll_chart_html = "<p>No payroll data available</p>"

    # ---------------- PROJECT PRIORITY ----------------
    project_df = pd.DataFrame(Projects.objects.values("priority"))
    if not project_df.empty:
        project_chart = px.bar(project_df["priority"].value_counts().reset_index(),
                               x="index", y="priority", color="index",
                               title="Projects by Priority")
        project_chart_html = project_chart.to_html(full_html=False)
    else:
        project_chart_html = "<p>No project data available</p>"

    # ---------------- LEAVE REQUESTS ----------------
    leave_df = pd.DataFrame(LeaveRequest.objects.values("status"))
    if not leave_df.empty:
        leave_chart = px.pie(leave_df, names="status", title="Leave Request Status")
        leave_chart_html = leave_chart.to_html(full_html=False)
    else:
        leave_chart_html = "<p>No leave data available</p>"

    # ---------------- NEW HIRES ----------------
    hire_df = pd.DataFrame(Employee.objects.values("hire_date"))
    if not hire_df.empty:
        hire_df["hire_date"] = pd.to_datetime(hire_df["hire_date"])
        hires_per_month = hire_df.groupby(hire_df["hire_date"].dt.strftime("%B"))["hire_date"].count().reset_index()
        hires_per_month.columns = ["Month", "New Hires"]
        hires_chart = px.line(hires_per_month, x="Month", y="New Hires", title="New Hires Trend")
        hires_chart_html = hires_chart.to_html(full_html=False)
    else:
        hires_chart_html = "<p>No hiring data available</p>"

    # ---------------- TOP PERFORMERS ----------------
    top_df = pd.DataFrame(Employee.objects.values("first_name", "last_name", "performance_score"))
    if not top_df.empty:
        top_df = top_df.sort_values(by="performance_score", ascending=False).head(5)
        top_df["Employee"] = top_df["first_name"] + " " + top_df["last_name"]
        top_chart = px.bar(top_df, x="Employee", y="performance_score", color="Employee",
                           title="Top Performers")
        top_chart_html = top_chart.to_html(full_html=False)
    else:
        top_chart_html = "<p>No performance data available</p>"

    # ---------------- RENDER TEMPLATE ----------------
    context = {
        "attendance_chart": attendance_chart_html,
        "employee_chart": employee_chart_html,
        "dept_chart": dept_chart_html,
        "payroll_chart": payroll_chart_html,
        "project_chart": project_chart_html,
        "leave_chart": leave_chart_html,
        "hires_chart": hires_chart_html,
        "top_chart": top_chart_html,
    }
    return render(request, "Admin/AdminPage.html", context)
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance, Payroll, LeaveRequest, MySkill, Meeting, Projects, Notifications, Employee

@login_required
def employee_dashboard(request):
    # Get logged-in employee object
    employee = Employee.objects.get(user=request.user)

    # ---------------- ATTENDANCE TREND ----------------
    attendance_data = Attendance.objects.filter(user=employee).values("date", "punch_in_time", "punch_out_time", "production_hours")
    attendance_df = pd.DataFrame(attendance_data)

    if not attendance_df.empty:
        attendance_df["date"] = pd.to_datetime(attendance_df["date"])
        attendance_chart = px.line(attendance_df, x="date", y="production_hours", title="Daily Attendance & Working Hours", markers=True)
        attendance_chart_html = attendance_chart.to_html(full_html=False)
    else:
        attendance_chart_html = "<p>No attendance data available</p>"

    # ---------------- LEAVE REQUEST STATUS ----------------
    leave_df = pd.DataFrame(LeaveRequest.objects.filter(employee=request.user).values("status"))
    if not leave_df.empty:
        leave_chart = px.pie(leave_df, names="status", title="Leave Request Status")
        leave_chart_html = leave_chart.to_html(full_html=False)
    else:
        leave_chart_html = "<p>No leave request data available</p>"

    # ---------------- PAYROLL SUMMARY ----------------
    payroll_df = pd.DataFrame(Payroll.objects.filter(employee=request.user).values("month", "net_salary"))
    if not payroll_df.empty:
        payroll_chart = px.bar(payroll_df, x="month", y="net_salary", color="month", title="Salary Summary")
        payroll_chart_html = payroll_chart.to_html(full_html=False)
    else:
        payroll_chart_html = "<p>No payroll data available</p>"

    # ---------------- SKILL PERFORMANCE ----------------
    skill_df = pd.DataFrame(MySkill.objects.filter(employee=employee).values("skill", "percentage"))
    if not skill_df.empty:
        skill_chart = px.bar(skill_df, x="skill", y="percentage", color="skill", title="Skill Performance (%)")
        skill_chart_html = skill_chart.to_html(full_html=False)
    else:
        skill_chart_html = "<p>No skill data available</p>"

    # ---------------- UPCOMING MEETINGS ----------------
    meetings = Meeting.objects.filter(participants=employee).order_by("date_meeting")[:5]

    # ---------------- ASSIGNED PROJECTS ----------------
    projects = Projects.objects.filter(user=request.user)

    # ---------------- LATEST NOTIFICATIONS ----------------
    notifications = Notifications.objects.filter(recipients=request.user).order_by("-created_at")[:5]

    context = {
        "attendance_chart": attendance_chart_html,
        "leave_chart": leave_chart_html,
        "payroll_chart": payroll_chart_html,
        "skill_chart": skill_chart_html,
        "meetings": meetings,
        "projects": projects,
        "notifications": notifications,
        "employee": employee,
    }
    return render(request, "Employee/EmployPage.html", context)
