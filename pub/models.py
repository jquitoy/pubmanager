from django.db import models

# Create your models here.

class Roles(models.Model):
  class Meta:
    db_table = 'tbl_roles'

  role_id = models.BigAutoField(primary_key=True, blank=False)
  role = models.CharField(max_length=55, blank=False)


class Staffs(models.Model):
  class Meta:
    db_table = 'tbl_staffs'

  staff_id = models.BigAutoField(primary_key=True, blank=False)
  full_name = models.CharField(max_length=55, blank=False)
  position = models.CharField(max_length=55, blank=False)
  email = models.EmailField(max_length=55, blank=False)
  role = models.ManyToManyField(Roles) 
  google_calendar_id = models.CharField(
    max_length=255,
    blank=True,
    default='primary'  # Default to their primary calendar
  )
 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Tasks(models.Model):
  class Meta:
    db_table = 'tbl_tasks'

  OBSERVANCE = 'OBS'
  COVERAGE = 'COV'
  TASK_TYPE_CHOICES = [
      (OBSERVANCE, 'Observance'),
      (COVERAGE, 'Coverage'),
  ]

  STATUS_CHOICES = [
      ('POSTED', 'Posted'),
      ('PENDING', 'Pending'),
      ('MISSED', 'Missed'),
      ('CANCELLED', 'Cancelled'),
  ]
  
  title = models.CharField(max_length=200)  # "Valentine’s Day Post"
  task_type = models.CharField(max_length=3, choices=TASK_TYPE_CHOICES)  # OBS/COV
  deadline = models.DateField()  # February 14, 5:00 PM
  description = models.TextField(blank=True)  # Optional details
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(  # Overall task status
      max_length=20,
      choices=STATUS_CHOICES,
      default='WORKING'
  )
  google_event_id = models.CharField(max_length=255, blank=True, null=True)  # For Google Calendar integration


class Assignments(models.Model):
    class Meta:
      db_table = 'tbl_assignments'
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)  # Links to the parent Task
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)  # Assigned staff member
    role = models.CharField(max_length=50)  # "WRITER", "DESIGNER" (from Staff.role)
    
    # Status (for staff progress)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),       # Assigned but not started
            ('ACCEPTED', 'Accepted'),     # Staff confirmed (for COVERAGE tasks)
            ('DECLINED', 'Declined'),     # Staff refused (for COVERAGE tasks)
            ('SUBMITTED', 'Submitted'),   # Work delivered
            ('MISSED', 'Missed Deadline'), 
        ],
        default='PENDING'
    )