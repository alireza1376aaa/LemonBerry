# Generated by Django 5.0.3 on 2024-06-24 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebLogSetting', '0010_uservisit_alter_site_setting_address_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservisit',
            name='date',
            field=models.DateField(),
        ),
    ]
