# Generated by Django 2.0.7 on 2018-10-07 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0021_auto_20181007_0224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_view_hris', 'View HRIS Database'),)},
        ),
    ]