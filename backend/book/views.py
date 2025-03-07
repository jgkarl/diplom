from django.shortcuts import render

# Create your views here.

def BookView(request):
    return render(request, 'book.html', {})