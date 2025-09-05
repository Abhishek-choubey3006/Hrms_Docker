from datetime import datetime, timedelta, date
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_aware, is_naive


# ======================== ROLE MODEL ========================
class Role(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


# ======================== EMPLOYEE MODEL ========================
class Employee(models.Model):
    Feature_image = models.ImageField(upload_to='media/Employee', blank=False, null=False)

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]
    Department = [
        ('UI/UX', 'UI/UX'), ('Development', 'Development'),
        ('Management', 'Management'), ('HR', 'HR'),
        ('Testing', 'Testing'), ('Marketing', 'Marketing'),
    ]
    Educations_Choices = [
        ('10TH', '10TH'), ('12TH', '12TH'), ('BACHELOR', 'BACHELOR'),
        ('MASTER', 'MASTER'), ('PHD', 'PHD'), ('OTHER', 'OTHER'),
        ('DIPLOMA', 'DIPLOMA'), ('CERTIFICATION', 'CERTIFICATION')
    ]
    Address_choices = [
        ('jharkhand', 'jharhand'), ('Bihar', 'Bihar'), ('UP', 'UP'), ('MP', 'MP'),
        ('Rajasthan', 'Rajasthan'), ('Punjab', 'Punjab'), ('Haryana', 'Haryana'),
        ('Delhi', 'Delhi'), ('Kashmir', 'Kashmir'), ('Goa', 'Goa'), ('Kerala', 'Kerala'),
        ('Tamil Nadu', 'Tamil Nadu'), ('Karnataka', 'Karnataka'), ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Telangana', 'Telangana'), ('Odisha', 'Odisha'), ('West Bengal', 'West Bengal'),
        ('Assam', 'Assam'), ('North East', 'North East'), ('Other', 'Other')
    ]
    Position_choices = [('Manager', 'Manager'), ('Team Lead', 'Team Lead'), ('Developer', 'Developer'),
                        ('Designer', 'Designer'), ('QA Engineer', 'QA Engineer'), ('HR', 'HR'),
                        ('Intern', 'Intern'), ('Other', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdaydate = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    department = models.CharField(choices=Department, default='Development', max_length=100)
    position = models.CharField(max_length=100, choices=Position_choices, default='Developer')
    hire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    Educations = models.CharField(choices=Educations_Choices, max_length=100, default='BACHELOR')
    Address = models.CharField(choices=Address_choices, max_length=150, default='Other')
    Country = models.CharField(default='India', max_length=100)
    Company = models.CharField(default='ABC Pvt Ltd', max_length=100)
    performance_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ======================== SKILL MODEL ========================
class MySkill(models.Model):
    Skill_choice = [
        ('Python', 'Python'), ('Django', 'Django'), ('JavaScript', 'JavaScript'),
        ('React', 'React'), ('Node.js', 'Node.js'), ('HTML', 'HTML'), ('CSS', 'CSS'),
        ('Java', 'Java'), ('C++', 'C++'), ('C#', 'C#'), ('Ruby', 'Ruby'), ('PHP', 'PHP'),
        ('Swift', 'Swift'), ('Kotlin', 'Kotlin'), ('Go', 'Go'), ('SQL', 'SQL'),
        ('NoSQL', 'NoSQL'), ('AWS', 'AWS'), ('Azure', 'Azure'), ('Docker', 'Docker'),
        ('Kubernetes', 'Kubernetes'), ('Machine Learning', 'Machine Learning'),
        ('Data Science', 'Data Science'), ('DevOps', 'DevOps'), ('UI/UX Design', 'UI/UX Design'),
        ('Project Management', 'Project Management'), ('Agile Methodologies', 'Agile Methodologies'),
        ('Scrum', 'Scrum'), ('Communication Skills', 'Communication Skills'),
        ('Problem Solving', 'Problem Solving'), ('Leadership', 'Leadership'),
        ('Time Management', 'Time Management'), ('Critical Thinking', 'Critical Thinking'),
        ('Collaboration', 'Collaboration'), ('Adaptability', 'Adaptability'),
        ('Creativity', 'Creativity'), ('Emotional Intelligence', 'Emotional Intelligence'),
        ('Conflict Resolution', 'Conflict Resolution'), ('Decision Making', 'Decision Making'),
        ('Networking', 'Networking'), ('Public Speaking', 'Public Speaking'),
        ('Writing Skills', 'Writing Skills'), ('Other', 'Other')
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.CharField(choices=Skill_choice, max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    percentage = models.IntegerField()


# ======================== NOTIFICATIONS MODEL ========================
class Notifications(models.Model):
    CHOICES = [('Recent', 'Recent'), ('Latest', 'Latest')]

    message = models.TextField()
    category = models.CharField(max_length=100, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User, related_name='notifications')

    def __str__(self):
        return self.message[:50]


# ======================== PAYROLL MODEL ========================
class Payroll(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    month = models.CharField(max_length=20, default="January")
    year = models.IntegerField(default=2025)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.hra - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.month} {self.year}"


# ======================== LEAVE REQUEST MODEL ========================
class LeaveRequest(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    CHOICES = [('Admin', 'Admin'), ('Employee', 'Employee')]

    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    target = models.CharField(max_length=50, choices=CHOICES, default='Employee')
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)
    some_date = models.DateField(default=date.today)
    admin_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.status}"

    @property
    def leave_days(self):
        return (self.end_date - self.start_date).days + 1


# ======================== LEAVE RECORD MODEL ========================
class LeaveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_leaves = models.IntegerField()
    taken = models.IntegerField()
    absent = models.IntegerField()
    request = models.IntegerField()
    worked_days = models.IntegerField()
    loss_of_pay = models.IntegerField()


# ======================== MEETING MODEL ========================
class Meeting(models.Model):
    msg_meeting = models.CharField(max_length=200, blank=False)
    date_meeting = models.DateTimeField(null=True, blank=True)
    time_meeting = models.TimeField(null=True, blank=True)
    Department = models.CharField(max_length=200)
    participants = models.ManyToManyField(Employee)


# ======================== EVENT MODEL ========================
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


# ======================== PROJECTS MODEL ========================
class Projects(models.Model):
    Priority = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    hour = models.IntegerField()
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(choices=Priority, max_length=100)


# ======================== JOB MODEL ========================
class Job(models.Model):
    gender = [('male', 'male'), ('female', 'female'), ('other', 'other')]
    department = [
        ('UI/UX', 'UI/UX'), ('Development', 'Development'),
        ('Management', 'Management'), ('HR', 'HR'),
        ('Testing', 'Testing'), ('Marketing', 'Marketing'),
    ]

    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone = models.IntegerField()
    Address = models.TextField()
    Resume = models.ImageField(upload_to='media/Resume', blank=False, null=False)
    Gender = models.CharField(choices=gender, max_length=15)
    Department = models.CharField(choices=department, max_length=40)
    Experince = models.CharField(max_length=20)


# ======================== ATTENDANCE MODEL ========================
class Attendance(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    punch_in_time = models.TimeField()
    punch_out_time = models.TimeField(null=True, blank=True)
    production_hours = models.FloatField(default=0.0)

    @property
    def total_duration(self):
        if self.punch_in_time and self.punch_out_time:
            in_datetime = datetime.combine(self.date, self.punch_in_time)
            out_datetime = datetime.combine(self.date, self.punch_out_time)

            if is_naive(in_datetime):
                in_datetime = make_aware(in_datetime)
            if is_naive(out_datetime):
                out_datetime = make_aware(out_datetime)

            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)

            return out_datetime - in_datetime
        return None

    def production_time(self):
        if self.punch_out_time:
            in_datetime = datetime.combine(self.date, self.punch_in_time)
            out_datetime = datetime.combine(self.date, self.punch_out_time)
            delta = out_datetime - in_datetime
            total_hours = round(delta.total_seconds() / 3600, 2)
            return total_hours
        return None

    @property
    def is_late(self):
        scheduled_time = datetime.strptime("09:00", "%H:%M").time()
        return self.punch_in_time > scheduled_time


# ======================== ACTIVITY LOG MODEL ========================
class ActivityLog(models.Model):
    user_name = models.CharField(max_length=100)
    user_role = models.CharField(max_length=100, blank=True)
    user_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    activity_text = models.TextField()
    project_name = models.CharField(max_length=100, blank=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.activity_text}"


# ======================== TASK MODEL ========================
class Task(models.Model):
    STATUS_CHOICES = [
        ('On Hold', '⏸ On Hold'),
        ('Completed', '✅ Completed'),
        ('Incomplete', '❌ Incomplete'),
        ('Pending', '⏳ Pending'),
        ('Received', '📥 Received'),
        ('In Progress', '⏳ In Progress')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ManyToManyField(User, related_name='tasks', blank=True)
    assign_to_all = models.BooleanField(default=False)

    def __str__(self):
        return self.title
