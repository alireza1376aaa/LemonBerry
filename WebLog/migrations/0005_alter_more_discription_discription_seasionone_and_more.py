# Generated by Django 5.0.3 on 2024-05-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebLog', '0004_more_discription_web_log_extra_discription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='more_discription',
            name='discription_seasionone',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='more_discription',
            name='discription_seasiontree',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='more_discription',
            name='discription_seasiontwo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='more_discription',
            name='title_seasionone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='more_discription',
            name='title_seasiontree',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='more_discription',
            name='title_seasiontwo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
