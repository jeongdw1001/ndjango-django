from django.shortcuts import render
from django.http import HttpResponse

'''
음식 사진 입력 모듈
'''

# 객체 검출 모델 및 추론 모듈은 별도의 restAPI 서버에 구현 후 api call을 통해 output만 받아서 화면에 디스플레이 하기


def view_e(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')