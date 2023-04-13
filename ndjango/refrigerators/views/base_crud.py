from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from refrigerators.forms import *
from refrigerators.models import Grocery
from django.core.files.storage import FileSystemStorage

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

# Create your views here.
def index(request):
    grocery_list = Grocery.objects.all().order_by('-id')
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_index.html', context)

def register(request):
    if request.method == 'POST':
        form = GrosForm(request.POST, request.FILES or None)
        if form.is_valid():
            grocery = form.save(commit=False)
            if request.FILES:
                grocery.image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(grocery.image.name, grocery.image)
            grocery.image = filename
            grocery.save()
            return redirect('refrigerators:index')
    else:
        form = GrosForm()       # form 생성
    context = {'form':form}
    return render(request, 'refrigerators/crud_register.html', context)

def view(request, pk):
    grocery_list = get_object_or_404(Grocery, id=pk)
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_view.html', context)

def edit(request, pk):
    post = get_object_or_404(Grocery, id=pk)
    if request.method == 'POST':
        form = GrosForm(request.POST, request.FILES, instance=post)
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
                if image:
                    # if a new image was uploaded, save it
                    filename = fs.save(image.name, image)
                    grocery.image = filename
                    # delete the old image file if it exists
                    if post.image:
                        fs.delete(post.image.name)
                else:
                    # keep the old image
                    grocery.image = post.image
            grocery.save()
            return redirect('refrigerators:index')
    else:
        form = GrosForm(instance=post)
    context = {'form': form}
    return render(request, 'refrigerators/crud_edit.html', context)


def delete(request, pk):
    grocery = get_object_or_404(Grocery, id=pk)
    grocery.delete()
    return redirect('refrigerators:index')