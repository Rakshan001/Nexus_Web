# Generated by Django 5.1.2 on 2024-10-31 05:00

import events_cec.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_cec', '0002_rename_title_event_event_title_remove_event_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventimage',
            name='image',
            field=models.ImageField(upload_to='event_images/', validators=[events_cec.models.validate_image_size]),
        ),
    ]