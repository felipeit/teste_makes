# Generated by Django 5.0.6 on 2024-05-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]