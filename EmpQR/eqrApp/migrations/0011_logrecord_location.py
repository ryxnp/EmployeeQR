# Generated by Django 4.2.16 on 2024-10-17 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eqrApp', '0010_alter_logrecord_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='logrecord',
            name='location',
            field=models.CharField(choices=[('location 1', 'Location 1'), ('location 2', 'Location 2'), ('location 3', 'Location 3'), ('location 4', 'Location 4'), ('location 5', 'Location 5')], max_length=10, null=True),
        ),
    ]
