from django.shortcuts import render
from .models import Item,Order,OrderItem
from django.http import JsonResponse  ,HttpResponse
from.models import OrderItem  

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm  # Assuming RegisterForm is defined in forms.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def home_view(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm

from .forms import CheckoutForm



def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    initial_data = {'key': 'value'}  # Replace with your initial data if needed

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('/')
    else:
        form = RegisterForm(initial=initial_data)

    return render(request, 'register.html', {'form': form})
class CustomLoginView(LoginView):
    form_class = LoginForm
    success_url = 'home/'  # Redirect to 'shop-home'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super().form_valid(form)
    
def cart_view(request):
       order_items = OrderItem.objects.filter(order__user=request.user, order__ordered=False)  
       total_cart_value = sum(item.get_total_item_price() for item in order_items)  
       return render(request, 'cart.html', {'order_items': order_items, 'total_cart_value': total_cart_value}) 


 
@login_required  
def add_to_cart(request, slug):  
    item = Item.objects.filter(slug=slug).first()  
    order_item, created = OrderItem.objects.get_or_create(  
        item=item,  
        user=request.user,  
    )  
    order_qs = Order.objects.filter(user=request.user, ordered=False).first()  
    if order_qs:  
        if order_qs.items.filter(item__slug=item.slug).exists():  
            order_item.quantity += 1  
            order_item.save()  
            messages.info(request, "This item quantity was updated.")  
        else:  
            order_qs.items.add(order_item)  
            order_qs.save()  
            messages.info(request, "This item was added to your cart.")  
    else:  
        order = Order.objects.create(user=request.user)  
        order.items.add(order_item)  
        order.save()  
        messages.info(request, "This item was added to your cart.")  
    return redirect('home') 






@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)    
    
   
def CheckoutView(request):

    order = Order.objects.get( ordered=False)
    form = CheckoutForm()
    context = {
                'form': form,
                'order': order,
            }
    return render(request, 'payment.html', context)
        
    
  