# Generated by Django 2.0 on 2020-06-10 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0037_auto_20200610_0236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='tour_booking',
            new_name='tour',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='tour_photo',
            new_name='tour',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='tour_review',
            new_name='tour',
        ),
    ]