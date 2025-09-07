from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions




urlpatterns = [
    path('', views.user_login, name='user_login'),  
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='user_logout'),
    path('employee/', views.EmployPage, name='employee_page'),
    path('adminpage/', views.AdminPage, name='admin_page'),
    # Employee All details
    path('Notification/', views.employee_Notification, name='employee_Notification'),
    path('apply-leave/', views.apply_leave_view, name='apply_leave'),
    path('leave-status/', views.leave_status_view, name='leave_status'),
    path('my-payroll/', views.view_my_payroll, name='view_my_payroll'),
    path('punch-in/', views.punch_in, name='punch_in'),
    path('punch-out/', views.punch_out, name='punch_out'),
    path('my-attendance/', views.punch_dashboard, name='punch_dashboard'),
    path('all-events/', views.all_events, name='all_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('calendar',views.test_calendar,name='calendar'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('manage-leave-requests/', views.admin_leave_requests_view, name='admin_leave_requests'),
    path('manage-payrolls/', views.manage_payrolls, name='manage_payrolls'),
    path('assign-project/', views.assign_project_view, name='assign_project'),
    path('create-task/',views.create_task_view, name='create_task'),
    path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('send-notification/',views.send_notification, name='send_notification'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# Visit:
# http://127.0.0.1:8000/swagger/
# Some things i have to install :pip install djangorestframework,pip install djangorestframework-simplejwt,pip install drf-yasg  and restframework configuration i had done update in rewuirement.txt