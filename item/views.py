from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from .forms import NewItemForm, EditItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def items(request):
    query = request.GET.get('query', 0)
    category_id = request.GET.get('category', 0)
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()


    return render(request, 'item/items.html', {
        'items':items,
        'query':query,
        'categories':categories,
        'category_id': int(category_id),
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request, 'item/detail.html', {
        'item':item,
        'related_items':related_items,
    })


# You have to be logged in to add new item ;)
@login_required
@staff_member_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {
        'form':form,
        'title': 'New Item',
    })
    
@login_required
@staff_member_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()
            
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
    return render(request, 'item/form.html', {
        'form':form,
        'title': 'Edit Item',
    })


@login_required
@staff_member_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect('dashboard:index')