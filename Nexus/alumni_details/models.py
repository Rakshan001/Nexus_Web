

# Alumni model
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os

def validate_image_size(image):
    max_size = 1 * 1024 * 1024  # 5 MB limit
    if image.size > max_size:
        raise ValidationError('Image file too large ( > 2MB )')

class Alumni(models.Model):
    alumni_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="alumni_profile")
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Allows optional phone number
    graduation_year = models.IntegerField(db_index=True)  # Added index for graduation year
    location = models.CharField(max_length=255, blank=True, null=True)  # Optional location
    profile_picture = models.ImageField(upload_to='photos/', blank=True, null=True, default='photos/default.png', validators=[validate_image_size])  # Add validator here
    batch = models.CharField(max_length=10)
    usn = models.CharField(max_length=20, unique=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)  # Optional LinkedIn URL
    current_position = models.CharField(max_length=255, db_index=True, null=True)
    branch = models.CharField(max_length=100, db_index=True)  # Added index for branch
    company_name = models.CharField(max_length=255, db_index=True, null=True)  # Added index for company name
    bio = models.TextField(blank=True, null=True)  # Optional bio
    achievements = models.TextField(blank=True, null=True)  # Optional achievements
    dob = models.DateField()
    is_alumni = models.BooleanField(default=True)
    personal_email = models.EmailField(blank=True, null=True, unique=True)  # Add personal email field

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
   


    class Meta:
        indexes = [
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['current_position']),
            models.Index(fields=['graduation_year']),  # Index for faster filtering by graduation year
            models.Index(fields=['branch']),  # Index for faster filtering by branch
            models.Index(fields=['company_name']),  # Index for faster filtering by company name
        ]
        # ordering = ['-graduation_year', 'first_name']  # Orders alumni by graduation year descending, then first name







''' Student details'''
# Student model
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    usn = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.usn})"






# CouncilMember model
class CouncilMember(models.Model):
    ROLE_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Joint Secretary', 'Joint Secretary'),
    ]

    count_mem_id = models.AutoField(primary_key=True)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name="council_members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.role} ({self.year}) - {self.alumni.first_name} {self.alumni.last_name}"

    class Meta:
        indexes = [
            models.Index(fields=['role']),  # Index for faster filtering by role
            models.Index(fields=['year']),  # Index for faster filtering by year
        ]
        unique_together = ('alumni', 'role', 'year')  # Ensures one role per alumni per year
