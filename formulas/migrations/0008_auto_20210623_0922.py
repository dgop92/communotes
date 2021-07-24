# Generated by Django 3.0.3 on 2021-06-23 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulas', '0007_auto_20210622_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='photo',
            field=models.ForeignKey(default=18, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='formulas.Photo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='formulas.Profile'),
            preserve_default=False,
        ),
    ]
