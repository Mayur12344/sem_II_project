# Generated by Django 4.1.4 on 2023-07-04 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btbookturf', '0015_booking_user_pk_myusers_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='user_pk',
        ),
    ]