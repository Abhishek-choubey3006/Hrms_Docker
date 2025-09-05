from django.contrib import admin
from .models import *
admin.site.register(Payroll)
admin.site.register(Employee)
admin.site.register(Notifications)
admin.site.register(Meeting)
admin.site.register(MySkill)
admin.site.register(LeaveRequest)
admin.site.register(LeaveRecord)
admin.site.register(Role)
admin.site.register(Projects)
admin.site.register(Task)
admin.site.register(Job)
admin.site.register(Event)
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['title', 'start_time', 'end_time', 'is_public']
#     list_filter = ['is_public', 'start_time']
# @admin.register(Attendance)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'punch_in_time', 'punch_out_time', 'production_hours')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'user__email')