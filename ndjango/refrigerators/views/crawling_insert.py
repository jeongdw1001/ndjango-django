from django.shortcuts import render
from django.http import HttpResponse

'''
크롤링 입력 모듈
'''


def view_c(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')