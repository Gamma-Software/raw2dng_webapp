# Generated by Django 4.1 on 2022-09-04 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raw2dng', '0005_alter_image_converted_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='converted_source',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
