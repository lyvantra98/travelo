# Generated by Django 2.0 on 2020-06-01 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0006_auto_20200601_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='destination',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tour.Destination'),
        ),
    ]