from .models import ActivityLog
from django.utils.timezone import now

def log_activity(user, activity_text, project_name=''):
    ActivityLog.objects.create(
        user_name=user.get_full_name() or user.username,
        user_role=getattr(user.staff_profile, 'position', ''),
        user_image=getattr(user.staff_profile, 'Feature_image', None),
        activity_text=activity_text,
        project_name=project_name,
        time=now().time(),
    )