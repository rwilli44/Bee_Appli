# Generated by Django 5.0.1 on 2024-01-11 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0016_alter_beeyard_beekeeper_alter_contamination_hive_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='treatment_type',
            field=models.CharField(choices=[('antifungal', 'Antifungal'), ('apivar', 'Apivar'), ('acide_oxalique', 'Acide Oxalique')], help_text='Name of the treatment applied to the hive', unique=True),
        ),
    ]
