# Generated by Django 2.0.7 on 2018-10-13 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0025_auto_20181013_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
    ]