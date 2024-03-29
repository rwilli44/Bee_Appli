# Generated by Django 5.0.1 on 2024-01-08 15:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0010_alter_intervention_content_type'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hive',
            name='queen_year',
            field=models.IntegerField(default=2024, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2040)]),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='content_type',
            field=models.ForeignKey(blank=True, help_text='For an Artificial Swarming select Apiary | Hive to select the CHILD hive. \n        For a treatment, select Apiary | Treatment to select the type of treatment. \n        Harvest and Syrup Distribution objects must be created before they can be selected for an intervention.', limit_choices_to=models.Q(models.Q(('app_label', 'apiary'), ('model', 'harvest')), models.Q(('app_label', 'apiary'), ('model', 'hive')), models.Q(('app_label', 'apiary'), ('model', 'syrupdistribution')), models.Q(('app_label', 'apiary'), ('model', 'treatment')), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='hive_affected',
            field=models.ForeignKey(help_text='The Hive concerned by the intervention. For Artificial Swarmings select the PARENT hive.', on_delete=django.db.models.deletion.CASCADE, to='apiary.hive'),
        ),
    ]
