# Generated by Django 2.0.7 on 2018-09-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0015_auto_20180921_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='building',
            field=models.CharField(blank=True, choices=[('R', 'Blessed Rebuschini Building'), ('L', 'Blessed Luigi Tezza Building'), ('1', 'St. Camillus Building - First floor'), ('2', 'St. Camillus Building - Second floor')], max_length=1),
        ),
    ]