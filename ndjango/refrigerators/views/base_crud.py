from django.shortcuts import render
from django.http import HttpResponse

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''


def view_b(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')