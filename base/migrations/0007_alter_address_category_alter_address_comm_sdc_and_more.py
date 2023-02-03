# Generated by Django 4.1.5 on 2023-01-27 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_resourcerouter_specs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='category',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='comm_sdc',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='dev_area',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='parish',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='post_code',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='settlement',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
