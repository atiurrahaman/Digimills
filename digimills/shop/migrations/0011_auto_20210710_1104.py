# Generated by Django 3.2.4 on 2021-07-10 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210710_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='default_address',
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='pincode',
            field=models.PositiveIntegerField(),
        ),
    ]