# Generated by Django 3.2.8 on 2022-02-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_postpicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpicture',
            name='image_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
