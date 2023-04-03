from django.urls import path, include
from recsys.views import recsys_2

'''
추천시스템 2 모듈
'''

urlpatterns = [
    path('recipes/diet', recsys_2.recipes_diet, name="rec-diet"),

]