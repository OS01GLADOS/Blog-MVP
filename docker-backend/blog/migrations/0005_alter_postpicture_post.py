# Generated by Django 3.2.8 on 2022-02-23 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_postpicture_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpicture',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
