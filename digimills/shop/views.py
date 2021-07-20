from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import JsonResponse


from .forms import CustomerForm, UserEditForm, UserSignUpForm
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .models import CustomerModel, Order, ProductModel, CartModel
from django.db.models import Q
from django.contrib.auth.models import User


class HomeView(View):  
    def get(self, request):
        cart_item_numbers = None
        if request.user.is_authenticated:
            cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        mobiles = ProductModel.objects.all().filter(product_category='M').order_by('?')[:4] 
        clothes = ProductModel.objects.all().filter(product_category='C').order_by('?')[:4]
        return render(request, 'shop/home.html', {'mobiles': mobiles, 'clothes':clothes, 'cart_item_numbers':cart_item_numbers})

    

def about(request):
    return render(request, 'shop/about.html')

@method_decorator(login_required, name='dispatch')
class AccountEditView(View):
    def get(self, request, username=None):
        cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        data = User.objects.get(username=username)
        form = UserEditForm(instance=data)
        return render(request, 'shop/account_edit.html', {'form':form, 'cart_item_numbers':cart_item_numbers})
    def post(self, request, username):
        data = User.objects.get(username=username)
        form = UserEditForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        return render(request, 'shop/profile.html', {'cart_item_numbers':cart_item_numbers})
            
@login_required
def show_cart(request):
    cart_item_numbers = None
    if request.user.is_authenticated:
        cart_item_numbers = len(CartModel.objects.filter(user=request.user))
    if cart_item_numbers:
        user = request.user
        cart = CartModel.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in CartModel.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        total_amount = amount + shipping_amount
        return render(request, 'shop/cart.html', {'carts':cart, 'totalamount':total_amount, 'shippingamount':shipping_amount, 'amount':amount, 'cart_item_numbers':cart_item_numbers})
    else:
        return render(request, 'shop/nocart.html', {'cart_item_numbers': cart_item_numbers})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('pro_id')
    product = ProductModel.objects.get(id=product_id)
    CartModel(user=user, product=product).save()
    return redirect('/cart')


@login_required
def plus_cart(request):
    if request.method == 'GET':
        pro_id = request.GET['pro_id']
        print(pro_id)
        c = CartModel.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in CartModel.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

        data= {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)
    else:
        return HttpResponse(" ")
@login_required
def minus_cart(request):
	if request.method == 'GET':
		pro_id = request.GET['pro_id']
		c = CartModel.objects.get(Q(product=pro_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in CartModel.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.selling_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def remove_cart(request):
	if request.method == 'GET':
		pro_id = request.GET['pro_id']
		c = CartModel.objects.get(Q(product=pro_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in CartModel.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)

@login_required
def checkout(request):
	add = CustomerModel.objects.filter(user=request.user)
	cart_items = CartModel.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in CartModel.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.selling_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'shop/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount,'totalitem':0, 'cart_item_numbers':0})

@login_required
def payment_done(request):
    usr = request.user
    custid = request.GET.get('custid')
    customer = CustomerModel.objects.get(id=custid)
    cart = CartModel.objects.filter(user=usr)
    for c in cart:
        Order(user=usr, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('/order/')
@login_required
def order(request):
    cart_item_numbers = len(CartModel.objects.filter(user=request.user))
    usr = request.user
    order = Order.objects.filter(user=usr).order_by('-order_date')
    return render(request, 'shop/order.html', {'order_placed':order, 'cart_item_numbers': cart_item_numbers})

def contact(request):
    return render(request, 'shop/contact.html')

def faq(request):
    return render(request, 'shop/faq.html')

class MobileView(View):
    def get(self, request, brand=None):
        cart_item_numbers = None
        if request.user.is_authenticated:
            cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        if brand == 'Redmi':
            mobiles = ProductModel.objects.filter(product_category='M').filter(product_brand=brand) 
        elif brand == 'Vivo':
            mobiles = ProductModel.objects.filter(product_category='M').filter(product_brand=brand) 
        elif brand == 'Oppo':
            mobiles = ProductModel.objects.filter(product_category='M').filter(product_brand=brand) 
        elif brand == 'Apple':
            mobiles = ProductModel.objects.filter(product_category='M').filter(product_brand=brand)
        else:
            mobiles = ProductModel.objects.filter(product_category='M')
        return render(request, 'shop/mobile.html', {'mobiles':mobiles, 'brand':brand, 'cart_item_numbers': cart_item_numbers}) 


def privacy(request):
    return render(request, 'shop/privacy.html')

class ProductSingleView(View):
    def get(self, request, pk):
        cart_item_numbers = None
        if request.user.is_authenticated:
            cart_item_numbers = len(CartModel.objects.filter(user=request.user))
            product = ProductModel.objects.get(id=pk)
            item_already_in_cart = False
            item_already_in_cart = CartModel.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'shop/product_single.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'cart_item_numbers': cart_item_numbers})
        else:
            product = ProductModel.objects.get(id=pk)
            return render(request, 'shop/product_single.html', {'product':product})

class ProductsView(View):
    def get(self, request):
        cart_item_numbers = None
        if request.user.is_authenticated:
            cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        products = ProductModel.objects.all()
        return render(request, 'shop/products.html', {'products':products, 'cart_item_numbers': cart_item_numbers})

@method_decorator(login_required, name='dispatch')
class ShowAddressView(View):
    def get(self, request):
        cart_item_numbers = len(CartModel.objects.filter(user=request.user))
        form = CustomerForm()
        addresses = CustomerModel.objects.filter(user=request.user.id)
        return render(request, 'shop/account_address.html', {'addresses':addresses, 'form':form, 'cart_item_numbers': cart_item_numbers})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            house_number = form.cleaned_data['house_number']
            street = form.cleaned_data['street']
            locality = form.cleaned_data['locality']
            district = form.cleaned_data['district']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            CustomerModel(user=user, name=name, mobile=mobile, house_number=house_number, street=street,locality=locality, district=district, state=state, pincode=pincode).save()
            
        return HttpResponseRedirect('/accounts/address/')

class UserRegister(View):
    def get(self, request):
        form = UserSignUpForm()
        return render(request, 'shop/register.html', {'form':form})
    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login/')
        return render(request, 'shop/register.html', {'form':form})

def terms(request):
    return render(request, 'shop/terms.html')

def user_detail(request, pk):
    return render(request, 'shop/user_detail.html')


