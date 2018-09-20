# Generated by Django 2.0.7 on 2018-09-07 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0011_drug_medication'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='indication',
            field=models.CharField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='drug',
            name='brand_name',
            field=models.CharField(blank=True, default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='drug',
            name='dosage',
            field=models.CharField(blank=True, default='', max_length=35),
        ),
    ]