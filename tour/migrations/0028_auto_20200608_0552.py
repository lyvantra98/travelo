# Generated by Django 2.0 on 2020-06-08 05:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0027_auto_20200608_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='The phone number you entered is not in the correct format', regex='((09|03|07|08|05)+([0-9]{8})\\b)')]),
        ),
    ]
