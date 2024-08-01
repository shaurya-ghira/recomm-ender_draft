# Generated by Django 5.0 on 2024-02-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='revenue',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
