# ndjango/refrigerators/models/__init__.py

from refrigerators.models.barcode_models import *
from refrigerators.models.base_models import *
from refrigerators.models.icon_models import *
from refrigerators.models.photo_models import *
from refrigerators.models.table_models import *

# app1 / submodels / model1.py file:
# from django.db import models
# class Store(models.Model):
#     class Meta:
#         app_label = "store"

# model3.py file:
#
# from django.db import models
# from app1.models import Store
#
# class Product(models.Model):
#     store = models.ForeignKey(Store)
#     class Meta:
#         app_label = "product"

# https://stackoverflow.com/questions/6336664/split-models-py-into-several-files