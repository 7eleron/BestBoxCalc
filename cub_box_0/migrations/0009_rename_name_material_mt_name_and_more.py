# Generated by Django 4.0.5 on 2022-06-20 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cub_box_0', '0008_material_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='material',
            old_name='name',
            new_name='mt_name',
        ),
        migrations.RenameField(
            model_name='material',
            old_name='type',
            new_name='mt_type',
        ),
    ]
