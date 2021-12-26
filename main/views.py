from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    return render(request, 'main.html')

def data(request):
    return render(request, 'data.html')

def struktur(request):
    return render(request, 'struktur.html')