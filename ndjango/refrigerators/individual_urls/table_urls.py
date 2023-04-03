from django.urls import path, include
from refrigerators.views import table_display

'''
냉장고 식재료 표(테이블) 제어 모듈
'''

urlpatterns = [
    path('f', table_display.view_f, name="view_f"),
]