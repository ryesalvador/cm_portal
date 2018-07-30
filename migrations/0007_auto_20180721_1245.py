# Generated by Django 2.0.7 on 2018-07-21 04:45

from django.db import migrations, models
import django_dropbox_storage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0006_auto_20180721_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, null=True, storage=django_dropbox_storage.storage.DropboxStorage(), upload_to='photos/employees/%Y/%m/%D'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='photo',
            field=models.ImageField(blank=True, null=True, storage=django_dropbox_storage.storage.DropboxStorage(), upload_to='photos/residents/%Y/%m/%D'),
        ),
    ]