# Generated by Django 5.1.3 on 2024-12-24 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_target_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('profile_view_student', 'Profile View by Student'), ('profile_view_alumni', 'Profile View by Alumni'), ('upcoming_event', 'Upcoming Event'), ('system', 'System Notification'), ('targeted', 'Targeted Notification'), ('contribution', 'Contribution Notification')], max_length=25),
        ),
    ]