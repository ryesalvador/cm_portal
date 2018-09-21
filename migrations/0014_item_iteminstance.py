# Generated by Django 2.0.7 on 2018-09-20 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cm_portal', '0013_auto_20180918_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=70)),
                ('brand_name', models.CharField(blank=True, max_length=70)),
                ('manufacturer', models.CharField(blank=True, max_length=70)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('MS', 'Medical supply'), ('ME', 'Medical equipment')], default='MS', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ItemInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateField()),
                ('expiration_date', models.DateField()),
                ('stocks_available', models.PositiveIntegerField(blank=True, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cm_portal.Item')),
            ],
        ),
    ]
