# Generated by Django 5.0.3 on 2024-06-08 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_inher', '0008_gallery_image4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='url_title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
