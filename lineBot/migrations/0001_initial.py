# Generated by Django 3.2.16 on 2022-12-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=100)),
                ('imgurAlbum', models.CharField(default='', max_length=20)),
                ('alias', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='LineChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=100)),
                ('userId', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('text', models.TextField(blank=True)),
                ('photoid', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupId', models.CharField(max_length=100)),
                ('userId', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=20)),
                ('imgurId', models.CharField(max_length=100)),
                ('photoDate', models.CharField(max_length=10)),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
