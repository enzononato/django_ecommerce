from django.http import HttpResponse
from django.shortcuts import render
def home_page(request):
    context = {
        "title": "Página principal",
        "content": "Bem-vindo a página principal"
    }
    return render(request, "index.html", context)

def about_page(request):
    context = {
        "title": "Sobre nós",
        "content": "Bem-vindo a página sobre nós"
    }
    return render(request, "about/view.html", context)

def contact_page(request):
    context = {
        "title": "Página de contato",
        "content": "Bem-vindo a página de contato"
    }
    return render(request, "contact/view.html", context)