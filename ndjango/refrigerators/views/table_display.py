from django.shortcuts import render
from django.http import HttpResponse

'''
냉장고 식재료 표(테이블) 제어 모듈
'''


def view_f(request):
    return HttpResponse('homepage')
    # return render(request, 'view_a.html')