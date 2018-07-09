from django.shortcuts import render
from .models import Post
def index(request):

    posts=Post.objects.all()
    return render(request,'app/stream.html')

def show(request,id):

    posts=Post.objects.get(pk=id)
    return render(request, 'app/show.html', {'posts':posts })
def map(request):
    return render(request, 'app/map.html',)
def data(request):
    return render(request,'app/data.html')