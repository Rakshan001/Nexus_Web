

# Create your models here.
from django.db import models

class ContactForm(models.Model):
    SUBJECT_CHOICES = [
        ('internship', 'Internship Offer'),
        ('job', 'Job Offer'),
        ('workshop', 'Workshop'),
        ('others', 'Others'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    branch = models.CharField(max_length=50)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    details = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
