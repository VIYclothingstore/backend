# from django.db import models
# from storages.backends.gcloud import GoogleCloudStorage
#
#
# class ProductPhotoStorage(GoogleCloudStorage):
#     bucket_name =
#
# class ProductCategory(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     image = models.ImageField(upload_to='products_images/')
#
#     category = models.ForeignKey(
#         ProductCategory,
#         on_delete=models.CASCADE,
#         related_name='products',
#     )
#
