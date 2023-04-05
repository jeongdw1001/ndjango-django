from django.urls import path, include
from recsys.views import recsys_1

'''
추천시스템 1 모듈
'''

urlpatterns = [
    path('recipes/ingredient', recsys_1.recipes_ingredient, name="rec-ingredient"),

]

def recing(input):
    