# Generated by Django 5.0.3 on 2024-05-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_inher', '0005_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='image',
            new_name='image1',
        ),
        migrations.AddField(
            model_name='gallery',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='upload/weblog/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='upload/weblog/%Y/%m/%d'),
        ),
    ]
