# Generated by Django 5.0.1 on 2024-01-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0008_alter_intervention_intervention_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(help_text='Quantity of the honey harvested in kilos')),
            ],
            options={
                'verbose_name': 'Harvest',
            },
        ),
        migrations.CreateModel(
            name='SyrupDistribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syrup_type', models.CharField(choices=[('Nectar', 'Nectar'), ('Cane Sugar', 'Cane Sugar'), ('White Sugar', 'White Sugar'), ('Raw Sugar', 'Raw Sugar')], help_text='The type of syrup provided to the hive')),
                ('quantity', models.FloatField(help_text='Quantity of the syrup provided in liters')),
            ],
            options={
                'verbose_name': 'Syrup Distribution',
            },
        ),
        migrations.DeleteModel(
            name='Quantity',
        ),
    ]
