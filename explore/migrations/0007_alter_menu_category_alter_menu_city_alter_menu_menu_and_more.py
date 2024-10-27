# Generated by Django 5.1.2 on 2024-10-26 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0006_alter_menu_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.CharField(blank=True, choices=[('Beef', 'Beef'), ('Chicken', 'Chicken'), ('Fish', 'Fish'), ('Lamb', 'Lamb'), ('Pork', 'Pork'), ('Rib Eye', 'Rib Eye'), ('Sirloin', 'Sirloin'), ('T-bone', 'T-Bone'), ('Tenderloin', 'Tenderloin'), ('Wagyu', 'Wagyu'), ('Other', 'Other')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='city',
            field=models.CharField(blank=True, choices=[('Central Jakarta', 'Central Jakarta'), ('East Jakarta', 'East Jakarta'), ('North Jakarta', 'North Jakarta'), ('South Jakarta', 'South Jakarta'), ('West Jakarta', 'West Jakarta')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='menu',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='restaurant_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='specialized',
            field=models.CharField(blank=True, choices=[('Argentinian', 'Argentinian'), ('Brazilian', 'Brazilian'), ('Breakfast Cafe', 'Breakfast Cafe'), ('British', 'British'), ('French', 'French'), ('Fushioned', 'Fushioned'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Local', 'Local'), ('Local Westerned', 'Local Westerned'), ('Mexican', 'Mexican'), ('Western', 'Western'), ('Singaporean', 'Singaporean')], max_length=50, null=True),
        ),
    ]