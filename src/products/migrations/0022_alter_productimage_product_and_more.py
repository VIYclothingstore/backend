# Generated by Django 4.2.11 on 2024-07-07 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0021_category_sub_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="products.productitem",
            ),
        ),
        migrations.AlterField(
            model_name="productitem",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="products.category",
            ),
        ),
        migrations.AlterField(
            model_name="warehouseitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wh_items",
                to="products.productitem",
            ),
        ),
    ]
