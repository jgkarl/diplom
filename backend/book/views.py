from django.shortcuts import render, redirect
from book.models import Book

# Create your views here.

def home(request):
    return render(request, "home.html")

def list(request):
    models = Book.objects.all()[:10]
    context = {"models": models}
    return render(request, "list.html", context)


# Model views
def details(request, pk):
    model = Book.objects.get(pk=pk)
    context = {"model": model}
    return render(request, "model/details.html", context)
