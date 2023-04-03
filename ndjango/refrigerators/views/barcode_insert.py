from django.shortcuts import render
from django.http import HttpResponse

'''
바코드 입력 모듈
'''


def view_a(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')