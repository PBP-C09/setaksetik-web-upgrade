# Generated by Django 5.1.4 on 2025-01-07 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meatup', '0009_alter_message_receiver_alter_message_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10),
        ),
    ]
