from django.urls import path, include
from recsys.views import recsys_3

'''
추천시스템 3 모듈
'''

urlpatterns = [
    path('random', recsys_3.random, name="rec-random"),

]