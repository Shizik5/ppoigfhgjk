# Generated by Django 4.2.2 on 2023-07-28 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_rename_title_filter_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filter',
            old_name='product',
            new_name='title',
        ),
    ]