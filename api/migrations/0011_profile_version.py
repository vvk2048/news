# Generated by Django 3.0.7 on 2020-09-03 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_news_etags'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='version',
            field=models.IntegerField(default=0),
        ),
    ]