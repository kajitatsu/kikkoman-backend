# Generated by Django 5.1.7 on 2025-03-31 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_restaurant_daycare_facility_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='retty_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Retty ID'),
        ),
    ]
