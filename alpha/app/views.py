from django.db.models.functions import Lower
from django.shortcuts import render
from django.template.defaultfilters import lower

from .models import Post, Site, Coordonates
def index(request):

    posts=Post.objects.all()
    return render(request,'app/stream.html')

def show(request,id):

    posts=Post.objects.get(pk=id)
    return render(request, 'app/show.html', {'posts':posts })
def map(request):
    return render(request, 'app/map.html',)
def data(request,id):
    coordonates=Coordonates.objects.filter(site_number=id)
    return render(request,'app/data.html',{'coordonates':coordonates})
def timeline(request):
    sites= Site.objects.all().order_by(Lower('id').desc())
    return render(request,'app/timeline.html',{'sites':sites})
def timeline_details(request,id):
    sites= Site.objects.get(site_number=id)
    return render(request,'app/timeline_details.html',{'sites':sites})