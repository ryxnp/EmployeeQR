# Generated by Django 4.2.16 on 2024-10-17 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eqrApp', '0011_logrecord_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logrecord',
            name='location',
            field=models.CharField(choices=[('location_1', 'Location 1'), ('location_2', 'Location 2'), ('location_3', 'Location 3'), ('location_4', 'Location 4'), ('location_5', 'Location 5')], max_length=10, null=True),
        ),
    ]
