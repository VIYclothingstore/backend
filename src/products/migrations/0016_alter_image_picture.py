# Generated by Django 4.2.11 on 2024-06-18 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0015_image_delete_productimage_product_image_urls"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="picture",
            field=models.ImageField(upload_to=""),
        ),
    ]
