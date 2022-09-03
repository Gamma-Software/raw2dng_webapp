# Generated by Django 4.1 on 2022-09-03 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('source', models.ImageField(upload_to='')),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
