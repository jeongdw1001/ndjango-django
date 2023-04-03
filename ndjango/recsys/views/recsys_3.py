from django.shortcuts import render
from django.http import HttpResponse

'''
추천시스템 3 모듈
'''


def random(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')