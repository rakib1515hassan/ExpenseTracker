# Generated by Django 5.0.6 on 2024-06-28 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0002_category_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.category', verbose_name='Category'),
        ),
    ]
