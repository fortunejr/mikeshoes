from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators  import login_required
from item.models import Item
from .models import CartItem

@login_required
def index(request, id):
    item = get_object_or_404(Item, id=id)
    cart = CartItem.objects.all()
    item_already_in_cart = False
    for x in cart:
        if item.description == x.description:
            item_already_in_cart = True
            print('Item already included')
            break
    if not item_already_in_cart:
        my_cart = CartItem.objects.create(
            
            name= item.name,
            description= item.description,
            price = item.price,
            image = item.image,
            is_sold = item.is_sold,
            created_by = request.user,
            created_at = item.created_at
        )
        my_cart.save()
        cart = CartItem.objects.filter(created_by=request.user)
    return render(request, 'cart/index.html',{
        'my_cart': cart,
    })

@login_required
def cart(request):
    cart = CartItem.objects.filter(created_by=request.user)
    return render(request,'cart/index.html',{
        'my_cart': cart,
    })

def detail(request, pk):
    item = get_object_or_404(CartItem, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    
    return render(request, 'cart/detail.html', {
        'item':item,
        'related_items':related_items,
    })

def delete(request):
    cart = CartItem.objects.all()
    cart.delete()
    return render(request,'cart/index.html',{
        'my_cart': cart,
    })
