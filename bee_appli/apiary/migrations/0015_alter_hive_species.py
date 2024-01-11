# Generated by Django 5.0.1 on 2024-01-11 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiary', '0014_hive_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hive',
            name='species',
            field=models.CharField(choices=[('black_bee', 'Black bee'), ('italian_bee', 'Italian bee'), ('caucasian_bee', 'Caucasian bee'), ('carnolian_bee', 'Carnolian bee'), ('buckfast_bee', 'Buckfast bee')], help_text='Type of bees'),
        ),
    ]