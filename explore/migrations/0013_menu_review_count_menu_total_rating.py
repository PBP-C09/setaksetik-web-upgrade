# Generated by Django 5.1.1 on 2025-01-09 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0012_alter_menu_claimed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='review_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='menu',
            name='total_rating',
            field=models.FloatField(default=0),
        ),
    ]
