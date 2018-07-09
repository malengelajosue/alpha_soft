from django.shortcuts import render

def home(request):


    return render(request,'home.html')
def error404(request):
    return  render(request,'error404.html',{}, status=404)