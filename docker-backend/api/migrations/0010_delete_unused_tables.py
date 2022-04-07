# Generated by Django 3.2.8 on 2022-04-07 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_delete_unused_tables'),
    ]

    operations = [
        migrations.RunSQL(
            'drop table if exists public.comments_comments cascade'
        ),
        migrations.RunSQL('drop table if exists public.user_profile cascade'),
        migrations.RunSQL('drop table if exists public.blog_post cascade'),
        migrations.RunSQL(
            'drop table if exists public.blog_postpicture cascade'
        ),
    ]
