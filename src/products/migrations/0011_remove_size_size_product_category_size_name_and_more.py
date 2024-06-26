# Generated by Django 4.2.11 on 2024-06-17 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0010_remove_product_category_product_gender_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="size",
            name="size",
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[("Чоловіки", "Чоловіки"), ("Жінки", "Жінки")],
                default="Футболки",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="size",
            name="name",
            field=models.CharField(default="M", max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.CharField(
                choices=[("Чоловіки", "Чоловіки"), ("Жінки", "Жінки")],
                default="Білий",
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="gender",
            field=models.CharField(
                choices=[("Чоловіки", "Чоловіки"), ("Жінки", "Жінки")],
                default="Чоловіки",
                max_length=15,
            ),
        ),
        migrations.DeleteModel(
            name="Color",
        ),
    ]
