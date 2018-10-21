# Generated by Django 2.0.7 on 2018-10-14 06:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0032_auto_20181014_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalequipment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular medical equipment across whole inventory', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='medicalsupply',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular medical supply across whole inventory', primary_key=True, serialize=False),
        ),
    ]