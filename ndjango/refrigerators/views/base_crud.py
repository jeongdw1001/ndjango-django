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

# Create your views here.
def index(request):
    grocery_list = Grocery.objects.all().order_by('-id')
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_index.html', context)

def register(request):
    if request.method == 'POST':
        form = GrocForm(request.POST, request.FILES)
        if form.is_valid():
            grocery = form.save(commit=False)
            if grocery.image:
                fs = FileSystemStorage()
                filename = fs.save(grocery.image.name, grocery.image)
                grocery.image = filename
            grocery.save()
            return redirect('refrigerators:index')
    else:
        form = GrocForm()
    context = {'form':form}
    return render(request, 'refrigerators/crud_register.html', context)
    
def view(request, pk):
    grocery_list = get_object_or_404(Grocery, id=pk)
    context = {'grocery_list': grocery_list}
    return render(request, 'refrigerators/crud_view.html', context)

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
        form = GrocForm(instance=post)
    context = {'form': form}
    return render(request, 'refrigerators/crud_edit.html', context)

def delete(request, pk):
    grocery = get_object_or_404(Grocery, id=pk)
    grocery.delete()
    return redirect('refrigerators:index')

def serve_grocery_image(request, pk):
    grocery = get_object_or_404(Grocery, pk=pk)
    if not grocery.image:
        raise Http404("Image not found")
    # construct the path to the image file
    path = os.path.join(settings.MEDIA_ROOT, str(grocery.image))
    # serve the image
    return serve(request, path, document_root=settings.MEDIA_ROOT)
