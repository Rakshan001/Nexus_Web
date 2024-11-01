# Generated by Django 5.1.2 on 2024-10-30 18:37

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
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('poster', models.ImageField(upload_to='event_posters/')),
                ('images', models.JSONField(blank=True, default=list)),
            ],
        ),
    ]
