# Generated by Django 5.1.1 on 2024-10-24 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spinthewheel', '0005_alter_spinhistory_spin_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Option',
        ),
    ]