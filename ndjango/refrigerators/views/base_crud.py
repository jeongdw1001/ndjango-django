from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from refrigerators.forms import *
from refrigerators.models import Grocery
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.static import serve
import os

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

# index 페이지 view
def index(request):
    grocery_list = Grocery.objects.all().order_by('-id')
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_index.html', context)

# 식재료 등록 페이지 view
def register(request):
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES)
        if form.is_valid():
            grocery = form.save(commit=False)
            image = request.FILES.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image.file)
                grocery.image = filename
            else :
                grocery.image = None
            grocery.save()
            return redirect('refrigerators:index')
    else:
        form = GrocForm()
    context = {'form':form}
    return render(request, 'refrigerators/crud_register.html', context)
    
# 식재료 상세 페이지 view
def view(request, pk):
    grocery_list = get_object_or_404(Grocery, id=pk)
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_view.html', context)

# 식재료 정보 수정 페이지 view
def edit(request, pk):
    post = get_object_or_404(Grocery, id=pk)
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            grocery = form.save(commit=False)
            fs = FileSystemStorage()
            if request.POST.get('image-clear'):  # check if image field was cleared
                # delete the old image file if it exists
                if post.image:
                    fs.delete(post.image.name)
                grocery.image = None
            else:
                image = request.FILES.get('image')
                if image: # 새로운 이미지가 업로드 되면
                    # delete old image
                    fs.delete(post.image.name)
                    # save new image
                    filename = fs.save(image.name, image.file)
                    grocery.image = filename
                else:
                    # keep the old image
                    grocery.image = post.image
            grocery.save()
            return redirect('refrigerators:index')
    else:
        form = GrocForm(instance=post)
    context = {'form': form}
    return render(request, 'refrigerators/crud_edit.html', context)

# 식재료 삭제 view
def delete(request, pk):
    grocery = get_object_or_404(Grocery, id=pk)
    grocery.delete()
    return redirect('refrigerators:index')

# 식재료 사진 view
def serve_grocery_image(request, pk):
    grocery = get_object_or_404(Grocery, pk=pk)
    if not grocery.image:
        raise Http404("Image not found")
    # construct the path to the image file
    path = os.path.join(settings.MEDIA_ROOT, str(grocery.image.name))
    # serve the image
    return serve(request, path, document_root=settings.MEDIA_ROOT)

# 식재료 구매 링크 view
#def buy(request, pk):
#    grocery = get_object_or_404(Grocery, id=pk)
#    name = grocery.name
#    return redirect("https://www.coupang.com/np/search?component=&q=%EC%82%AC%EA%B3%BC&channel=user")