from django.db import models

class FacultyCoordinator(models.Model):
    coordinator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Coordinator's name
    department= models.CharField(max_length=100)  # Coordinator's branch (department)
    email = models.EmailField(unique=True)  # Coordinator's email address
    phone_number = models.CharField(max_length=15)  # Coordinator's phone number


    def __str__(self):
        return self.name

class StudentCoordinator(models.Model):
    coordinator_id =models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  # Coordinator's name
    branch= models.CharField(max_length=100)  # Coordinator's branch (department)
    email = models.EmailField(unique=True)  # Coordinator's email address
    phone_number = models.CharField(max_length=15)  # Coordinator's phone number


    def __str__(self):
        return self.name
