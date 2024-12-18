# Generated by Django 5.1.3 on 2024-12-15 21:51

import colorfield.fields
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('emoji', models.CharField(blank=True, max_length=2, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='categories/icons/')),
                ('background_color', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='categories.category')),
            ],
        ),
    ]