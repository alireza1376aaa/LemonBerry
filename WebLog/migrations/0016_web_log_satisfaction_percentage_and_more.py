# Generated by Django 5.0.3 on 2024-06-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebLog', '0015_alter_rate_of_blog_weblod'),
    ]

    operations = [
        migrations.AddField(
            model_name='web_log',
            name='satisfaction_percentage',
            field=models.IntegerField(default=0, max_length=3),
        ),
        migrations.AlterField(
            model_name='rate_of_blog',
            name='score',
            field=models.IntegerField(default=0, max_length=3),
        ),
    ]
