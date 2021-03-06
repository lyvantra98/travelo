# Generated by Django 3.0.3 on 2020-07-12 03:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0005_auto_20200705_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='like',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(upload_to='images/blogs/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Số điện thoại không đúng định dạng', regex='((09|03|07|08|05)+([0-9]{8})\\b)')]),
        ),
    ]
