# Generated by Django 5.0.3 on 2024-06-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebLog', '0009_web_log_main_title_alter_web_log_category_web_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='web_log',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
