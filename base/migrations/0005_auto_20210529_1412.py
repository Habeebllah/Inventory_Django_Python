# Generated by Django 3.2 on 2021-05-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_orderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ref_code',
        ),
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
