# Generated by Django 2.2.9 on 2020-01-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pID', models.TextField()),
                ('title', models.CharField(max_length=50)),
                ('cover', models.ImageField(upload_to='')),
                ('creator', models.CharField(max_length=50)),
            ],
        ),
    ]
