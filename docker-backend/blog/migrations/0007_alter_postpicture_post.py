# Generated by Django 3.2.8 on 2022-02-24 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_postpicture_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpicture',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pics', to='blog.post'),
        ),
    ]
