# Generated by Django 5.0.1 on 2024-01-05 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0003_alter_intervention_content_type_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hive',
            options={'verbose_name': 'Hive'},
        ),
        migrations.AlterField(
            model_name='intervention',
            name='content_type',
            field=models.ForeignKey(blank=True, help_text='For interventions requiring a quantity (Harvest, Syrup) select Apiary | Quantity. \n        For an Artificial Swarming select Apiary | Hive to select the parent hive. \n        For a treatment, select Apiary | treatment to select the type of treatment. \n        Quantity and treatment objects must be created before they can be selected for an intervention.', limit_choices_to=models.Q(models.Q(('app_label', 'apiary'), ('model', 'quantity')), models.Q(('app_label', 'apiary'), ('model', 'hive')), models.Q(('app_label', 'apiary'), ('model', 'treatment')), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='hive_affected',
            field=models.ForeignKey(help_text='The Hive concerned by the intervention. For Artificial Swarmings select the child hive.', on_delete=django.db.models.deletion.CASCADE, to='apiary.hive'),
        ),
    ]
