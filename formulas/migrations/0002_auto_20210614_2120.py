# Generated by Django 3.0.3 on 2021-06-15 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='path',
            new_name='content',
        ),
    ]
