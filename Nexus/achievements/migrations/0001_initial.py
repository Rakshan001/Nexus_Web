# Generated by Django 4.2.1 on 2024-10-05 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alumni_details', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('achievement_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_achieved', models.DateField()),
                ('category', models.CharField(max_length=100)),
                ('alumni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alumni_details.alumni')),
            ],
        ),
    ]