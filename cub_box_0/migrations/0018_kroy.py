# Generated by Django 4.1.1 on 2023-03-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cub_box_0', '0017_alter_work_options_alter_work2_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kroy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('kroy_Img', models.ImageField(upload_to='images_kroy/')),
            ],
        ),
    ]
