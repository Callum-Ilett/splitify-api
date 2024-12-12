# Generated by Django 5.1.3 on 2024-12-12 13:14

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
        ('groups', '0002_group_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='associated_groups', to='currency.currency'),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('member', 'Member'), ('owner', 'Owner')], default='member', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='groups.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='joined_groups', through='groups.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
    ]