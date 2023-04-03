from django.shortcuts import render
from django.http import HttpResponse

'''
추천시스템 2 모듈
'''


def recipes_diet(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')