# Generated by Django 4.0.5 on 2022-06-19 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='user_image',
            field=models.ImageField(default='user.png', upload_to='user_image/'),
        ),
    ]
