# Generated by Django 5.0.3 on 2024-06-08 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebLog', '0008_alter_web_log_date'),
        ('Web_inher', '0009_alter_tag_url_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='web_log',
            name='main_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='web_log',
            name='category_web_model',
            field=models.ManyToManyField(blank=True, null=True, to='Web_inher.category_web'),
        ),
    ]
