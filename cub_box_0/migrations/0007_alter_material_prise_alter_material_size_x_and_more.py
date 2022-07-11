# Generated by Django 4.0.5 on 2022-06-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cub_box_0', '0006_alter_material_prise_alter_material_size_x_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='prise',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='size_x',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='size_y',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Close_fitting',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Content',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Lid',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Scotch',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='Tray',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='dm2',
            field=models.IntegerField(null=True),
        ),
    ]