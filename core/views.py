from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignUpForm
from django.contrib.auth import logout, login

def index(request):
    items = Item.objects.filter(is_sold=False) # Getting the all newest unsold products
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {
        'form': form
    })


def logoutuser(request):
    logout(request)
    return render(request, 'core/index.html')