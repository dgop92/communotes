# Generated by Django 3.0.3 on 2021-06-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulas', '0008_auto_20210623_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.SlugField(max_length=80, unique=True),
        ),
    ]