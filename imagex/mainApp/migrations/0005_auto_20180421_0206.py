# Generated by Django 2.0.3 on 2018-04-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20180409_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
