from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request=request, template_name='home/home.html')


def about(request):
    return render(request=request, template_name='home/about.html')

