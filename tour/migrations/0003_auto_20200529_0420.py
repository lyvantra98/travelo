# Generated by Django 2.0 on 2020-05-29 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_auto_20200529_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(0, 'Male'), (1, 'Female')], null=True),
        ),
    ]
