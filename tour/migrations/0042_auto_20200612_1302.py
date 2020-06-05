# Generated by Django 3.0.3 on 2020-06-12 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0041_auto_20200612_0843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='destination',
        ),
        migrations.AddField(
            model_name='destination',
            name='tour',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tour.Tour'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
