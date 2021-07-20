# Generated by Django 3.2.4 on 2021-07-10 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered')], default='Pending', max_length=10),
        ),
    ]
