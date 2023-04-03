from django.shortcuts import render
from django.http import HttpResponse

'''
추천시스템 1 모듈
'''


def recipes_ingredient(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')