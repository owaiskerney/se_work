# Generated by Django 2.0.3 on 2018-04-20 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_auto_20180421_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[['Abstract', 'Abstract'], ['Aerial', 'Aerial'], ['Animals', 'Animals'], ['Architecture', 'Architecture'], ['Black and White', 'Black and White'], ['Family', 'Family'], ['Fashion', 'Fashion'], ['Fine Art', 'Fine Art'], ['Food', 'Food'], ['Journalism', 'Journalism'], ['Landscape', 'Landscape'], ['Macro', 'Macro'], ['Nature', 'Nature'], ['Night', 'Night'], ['People', 'People'], ['Performing Arts', 'Performing Arts'], ['Sport', 'Sport'], ['Still Life', 'Still Life'], ['Street', 'Street'], ['Travel', 'Travel']], max_length=30),
        ),
    ]
