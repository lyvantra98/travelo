# Generated by Django 2.0 on 2020-06-10 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0036_auto_20200610_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='tour_review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_r', to='tour.Tour'),
        ),
    ]