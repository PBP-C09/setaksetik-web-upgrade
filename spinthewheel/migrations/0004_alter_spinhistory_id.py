# Generated by Django 5.1.1 on 2024-10-22 13:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spinthewheel', '0003_spinhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spinhistory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
