# Generated by Django 3.0.7 on 2020-08-30 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_mycategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycategory',
            old_name='category',
            new_name='categorys',
        ),
    ]
