# Generated by Django 3.2.8 on 2022-02-23 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_postpicture_image_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpicture',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]