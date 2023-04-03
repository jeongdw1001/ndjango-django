from django.urls import path, include
from refrigerators.views import crawling_insert

'''
크롤링 입력 모듈
'''

urlpatterns = [
    path('c', crawling_insert.view_c, name="view_c"),
]