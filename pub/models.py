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
