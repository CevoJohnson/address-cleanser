# Generated by Django 4.1.5 on 2023-01-29 02:36

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_address_pindex'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='address',
            index=django.contrib.postgres.indexes.GinIndex(fields=['dev_area'], name='dIndex', opclasses=['gin_trgm_ops']),
        ),
        migrations.AddIndex(
            model_name='address',
            index=django.contrib.postgres.indexes.GinIndex(fields=['comm_sdc'], name='cIndex', opclasses=['gin_trgm_ops']),
        ),
    ]