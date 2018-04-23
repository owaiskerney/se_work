# Generated by Django 2.0.4 on 2018-04-23 14:25

from django.db import migrations
import mainApp.validators
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=stdimage.models.StdImageField(blank=True, upload_to='avatars/', validators=[mainApp.validators.validate_file_extension]),
        ),
    ]
