from django.urls import path, include
from refrigerators.views import base_crud

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

urlpatterns = [
    path('b', base_crud.view_b, name="view_b"),
]