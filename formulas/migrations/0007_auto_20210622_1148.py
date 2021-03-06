# Generated by Django 3.0.3 on 2021-06-22 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulas', '0006_auto_20210622_1113'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('photo', 'profile'), name='one review per photo'),
        ),
    ]
