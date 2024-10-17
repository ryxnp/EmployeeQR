from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from PIL import Image
from django.core.exceptions import ValidationError

class Employee(models.Model):
    employee_code = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=(("Male","Male"), ("Female","Female")), default="Male")
    dob = models.DateField(max)
    contact = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=250, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    department = models.TextField(null=True, blank=True)
    position = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to = "employee-avatars/",null=True, blank=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(f"{self.employee_code} - {self.first_name} "+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )
    def name(self):
        return str(f"{self.first_name} "+ (f"{self.middle_name} {self.last_name}" if not self.middle_name == "" else f"{self.last_name}") )


    def save(self, *args, **kwargs):
        if self.avatar:  # Ensure there's an avatar before processing
            super(Employee, self).save(*args, **kwargs)  # Save first to get the path
            try:
                imag = Image.open(self.avatar.path)
                if imag.width > 200 or imag.height > 200:
                    output_size = (200, 200)
                    imag.thumbnail(output_size)
                    imag.save(self.avatar.path)
            except Exception as e:
                raise ValidationError(f"Error processing image: {e}")
        else:
            super(Employee, self).save(*args, **kwargs)  # Save without processing if no avatar
        
class LogRecord(models.Model):
    ACTION_CHOICES = [
        ('time_in', 'Time In'),
        ('time_out', 'Time Out'),
    ]
    LOCATION_CHOICES = [
        ('location_1', 'Location 1'),
        ('location_2', 'Location 2'),
        ('location_3', 'Location 3'),
        ('location_4', 'Location 4'),
        ('location_5', 'Location 5'),
    ]

    employee_pk = models.ForeignKey(Employee, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    time = models.DateTimeField()
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_pk.first_name} {self.employee_pk.last_name} - {self.get_action_display()}"

    def print_time(self):
        """Return formatted string of time-in and time-out."""
        return self.time.strftime('%H:%M:%S')


