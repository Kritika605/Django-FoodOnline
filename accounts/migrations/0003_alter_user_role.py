# Generated by Django 4.1.7 on 2023-04-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Vendor'), (2, 'Customer')], null=True),
        ),
    ]