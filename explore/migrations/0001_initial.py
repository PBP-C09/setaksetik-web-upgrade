# Generated by Django 5.1.1 on 2025-01-11 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.core.management import call_command


class Migration(migrations.Migration):

    def load_my_initial_data(apps, schema_editor):
        call_command("loaddata", "data.json")

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('menu', models.CharField(blank=True, max_length=50, null=True)),
                ('restaurant_name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(blank=True, choices=[('Beef', 'Beef'), ('Chicken', 'Chicken'), ('Fish', 'Fish'), ('Lamb', 'Lamb'), ('Pork', 'Pork'), ('Rib Eye', 'Rib Eye'), ('Sirloin', 'Sirloin'), ('T-bone', 'T-Bone'), ('Tenderloin', 'Tenderloin'), ('Wagyu', 'Wagyu'), ('Other', 'Other')], max_length=50, null=True)),
                ('city', models.CharField(blank=True, choices=[('Central Jakarta', 'Central Jakarta'), ('East Jakarta', 'East Jakarta'), ('North Jakarta', 'North Jakarta'), ('South Jakarta', 'South Jakarta'), ('West Jakarta', 'West Jakarta')], max_length=50, null=True)),
                ('specialized', models.CharField(blank=True, choices=[('Argentinian', 'Argentinian'), ('Brazilian', 'Brazilian'), ('Breakfast Cafe', 'Breakfast Cafe'), ('British', 'British'), ('French', 'French'), ('Fushioned', 'Fushioned'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Local', 'Local'), ('Local Westerned', 'Local Westerned'), ('Mexican', 'Mexican'), ('Western', 'Western'), ('Singaporean', 'Singaporean')], max_length=50, null=True)),
                ('takeaway', models.BooleanField(blank=True, null=True)),
                ('delivery', models.BooleanField(blank=True, null=True)),
                ('outdoor', models.BooleanField(blank=True, null=True)),
                ('smoking_area', models.BooleanField(blank=True, null=True)),
                ('wifi', models.BooleanField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('review_count', models.IntegerField(default=0)),
                ('total_rating', models.FloatField(default=0)),
                ('claimed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claimed_menus', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(load_my_initial_data),
    ]
