# Generated by Django 3.0.7 on 2020-09-20 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200920_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='newsAgency',
            field=models.CharField(default='Independent', max_length=512),
        ),
    ]
