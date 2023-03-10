# Generated by Django 4.1.5 on 2023-01-16 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_parishe_rename_counties_countie_delete_parish'),
    ]

    operations = [
        migrations.AddField(
            model_name='parishe',
            name='county_located_in',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parishe',
            name='perimeter',
            field=models.FloatField(blank=True),
        ),
    ]
