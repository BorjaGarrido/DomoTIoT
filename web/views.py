from django.shortcuts import render

# Create your views here.

def modulo_list(request):
    return render(request, 'web/modulo_list.html', {})
