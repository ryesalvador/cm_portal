# Generated by Django 2.0.7 on 2018-10-13 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0024_auto_20181013_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='resident',
            field=models.ForeignKey(limit_choices_to={'vital_status': 'LI'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='cm_portal.Resident'),
        ),
    ]