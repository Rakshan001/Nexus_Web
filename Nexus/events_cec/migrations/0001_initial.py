# Generated by Django 5.1.4 on 2024-12-24 18:58

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
                ('category', models.CharField(choices=[('workshop', 'Workshop'), ('talk', 'Alumni Talk'), ('others', 'Others')], max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True)),
                ('location', models.CharField(max_length=200)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='event_posters/')),
                ('instagram_url', models.URLField(blank=True, max_length=500, null=True)),
                ('facebook_url', models.URLField(blank=True, max_length=500, null=True)),
                ('youtube_url', models.URLField(blank=True, max_length=500, null=True)),
                ('linkedin_url', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_uploaded'],
            },
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
