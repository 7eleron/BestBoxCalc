from django.http.response import HttpResponse
from django.shortcuts import render


def first_page(request):
    text = 'New text'
    a = 'Hello world'
    return render(request, './index.html')