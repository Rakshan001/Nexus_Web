# Generated by Django 5.1.2 on 2024-10-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_details', '0002_alumni_personal_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='profile_picture',
            field=models.ImageField(blank=True, default='photos/default.png', null=True, upload_to='photos/'),
        ),
    ]
