# Generated by Django 5.1.2 on 2024-12-07 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meatup', '0006_remove_wishlist_owner_message_delete_meatuprequest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
