from django.db import migrations
import uuid

def generate_uuid(apps, schema_editor):
    Alumni = apps.get_model('alumni_details', 'Alumni')
    for alumni in Alumni.objects.all():
        if not alumni.uuid:
            alumni.uuid = uuid.uuid4()
            alumni.save()

class Migration(migrations.Migration):
    dependencies = [
        ('alumni_details', '0009_alumni_uuid_alter_alumni_graduation_year'),
    ]

    operations = [
        migrations.RunPython(generate_uuid),
    ]