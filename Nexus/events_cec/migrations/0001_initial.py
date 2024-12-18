# Generated by Django 5.1.2 on 2024-11-02 06:28

import django.db.models.deletion
import events_cec.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='event_posters/')),
            ],
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='event_images/', validators=[events_cec.models.validate_image_size])),
                ('event', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='event_images', to='events_cec.event')),
            ],
        ),
    ]
