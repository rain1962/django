# Generated by Django 3.0.2 on 2020-02-13 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20200213_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='createdtime',
            field=models.TextField(max_length=32),
        ),
    ]
