# Generated by Django 3.1.7 on 2021-06-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210601_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.CharField(default='_', max_length=50),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(default='_', max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='road_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='country',
            name='code',
            field=models.CharField(default='_', max_length=120),
        ),
        migrations.AlterField(
            model_name='country',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='country',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(default='_', max_length=120),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(default='_', max_length=120),
        ),
    ]
