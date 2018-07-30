# Generated by Django 2.0.7 on 2018-07-21 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0004_auto_20180721_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='physicians',
            field=models.ManyToManyField(blank=True, null=True, to='cm_portal.Physician'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='relatives',
            field=models.ManyToManyField(null=True, to='cm_portal.Relative'),
        ),
    ]