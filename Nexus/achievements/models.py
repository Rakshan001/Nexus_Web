# achievements/models.py

from django.db import models
from alumni_details.models import Alumni  # Adjust the import based on your actual Alumni model location

class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    description = models.TextField()
    date_achieved = models.DateField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
