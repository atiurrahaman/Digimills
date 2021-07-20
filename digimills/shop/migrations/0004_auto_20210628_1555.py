# Generated by Django 3.2.4 on 2021-06-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_customermoder_customermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressmodel',
            name='pincode',
            field=models.PositiveIntegerField(default=0, max_length=6),
        ),
        migrations.AlterField(
            model_name='addressmodel',
            name='house_number',
            field=models.PositiveIntegerField(),
        ),
    ]
