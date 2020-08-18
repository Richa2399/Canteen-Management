from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login,logout
from . models import Customer
User=get_user_model()
from app1.models import Category,Menu,Cart,Myorder,Orders,Ingredients
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
from . form import *

#MID='eEBWPB26257464899048'
#MKEY='&aNqcrbno!fZ1RIw'
MID='BJcRTy97367256751460'
MKEY='OY8#C1mBOBoA2NHK'

# Create your views here.
def indexPage(request):
	cat=Category.objects.all()
	menu=Menu.objects.all()
	return render(request,'app/index.html',{'category':cat,'menu':menu})

def registerPage(request):
	
	if request.method=='POST':
		Phone=request.POST.get('phone')
		try:
			User.objects.get(username=Phone)
			return render(request,'app/register.html',{'message':'Phone Number Taken'})

		except:	
			First_Name=request.POST.get('fname')
			Last_Name=request.POST.get('lname')
		
			coll_id=request.POST.get('coll_id')
			email =request.POST.get('email')
			pasword=request.POST.get('pasword2')
			designation=request.POST.get('designation')
			colid=request.FILES['id_image']
			fs = FileSystemStorage()
			filename = fs.save(colid.name, colid)

			if designation=='staff':
				user_obj=User.objects.create_user(username=Phone,password=pasword,email=email,is_student=False,is_staff=True,first_name=First_Name,last_name=Last_Name,phone=Phone,profile=colid.name)
				Customer.objects.create(customer=user_obj,college_id=coll_id,idImage=colid.name)
			else:
				user_obj=User.objects.create_user(username=Phone,password=pasword,email=email,is_student=True,is_staff=False,first_name=First_Name,last_name=Last_Name,phone=Phone)
				Customer.objects.create(customer=user_obj,college_id=coll_id,idImage=colid.name)
			return redirect(login_page)

	else:
		return render(request,'app/register.html')

 

 
@csrf_exempt
def handlerequest(request): #paytm will send POST request herre
	if request.method=='POST':
		form = request.POST
		response_dict = {}
		for i in form.keys():
			response_dict[i] = form[i]
			if i == 'CHECKSUMHASH':
				checksum = form[i]
		verify = Checksum.verify_checksum(response_dict, MKEY, checksum)
		print(response_dict)
	
		if verify:
			if response_dict['RESPCODE'] == '01':
				print('order successful')
				idlist=response_dict['ORDERID'].split('-')
				for i in idlist:
					ord=Orders.objects.get(id=i)
					ord.payment_status='Paid'
					ord.transaction_id=response_dict['TXNID']
					ord.save()

			else:
				print('order was not successful because' + response_dict['RESPMSG'])
		return render(request, 'app/payment_status.html', {'response': response_dict})

	else:
		return redirect(menu)
 
 

# def canteenregisterpage(request):
# 	if request.method=='POST':
# 		name=request.POST.get('name')
# 		Phone=request.POST.get('phone')
# 		# enrollment=request.POST.get('enrollment')
# 		email =request.POST.get('email ')
# 		pasword=request.POST.get('pasword2')
	
# 		user_obj=User.objects.create_user(username=Phone,password=pasword,email=email,is_restaurant=True,is_student=False,is_staff=False,first_name=name,phone=Phone)
# 		return redirect(login_page)
# 	else:
# 		return render(request,'app/canteenregister.html')
	

def login_page(request):
		if request.method=='POST':
			phone=request.POST.get('phone')
			password=request.POST.get('password')

			user=authenticate(username=phone,password=password)
			if user:
				if user.is_restaurant==True:
					cant=CanteenProfile.objects.get(canteen=user)
					if cant.status=='Block':
						return render(request,'app1/canlogin.html',{'message':'Account Blocked By Admin'})
					else:
						login(request,user)
						return redirect('index_canteen')
				else:
					login(request,user)
					return redirect(indexPage)
			else:

				return render(request,'app/login.html',{'message':'Invalid email or password'})
		else:
			return render(request,'app/login.html')

def logout_user(request):

	logout(request)
	return redirect(login_page)


def menu(request,*args):
	obj=Menu.objects.all()
	cat=Category.objects.all()
	canteen=User.objects.filter(is_restaurant=True)
	if request.user.is_authenticated:
		cart=Cart.objects.filter(customer=request.user)
		no_of_items=len(list(cart))
		print(no_of_items,'no of items')
		total=cart.aggregate(Sum('price'))
		return render(request,'app/menu.html',{'menu':obj,'cart':cart,'cat':cat,'total':total,'items':no_of_items,'canteen':canteen})
	else:
		return render(request,'app/menu.html',{'menu':obj,'cat':cat,'canteen':canteen,'items':0})
	print(obj)
	

@login_required(login_url='/login/')
def add_cart(request,pk):
	if request.user.is_restaurant==True:
		logout(request)
		return render(request,'app\only_customer.html')
	food=Menu.objects.get(pk=pk)
	print(food.canteen)
	#canobj=User.objects.get(id=food.canteen)
	try:
		obj=Cart.objects.get(food=food,customer=request.user)
		obj.quantity=obj.quantity+1
		p=obj.food.price
		obj.price=p*obj.quantity
		obj.save()
	except:
			
		Cart.objects.create(customer=request.user,food=food,price=food.price,canteen=food.canteen)
	
	return redirect(menu)

def delete_cart(request,pk):
	obj=Cart.objects.get(pk=pk)
	obj.delete()
	return redirect(menu)

	'''
	obj.quantity+=1
	obj.save()

	'''
def plus_item(request,pk):
	obj=Cart.objects.get(pk=pk)
	obj.quantity+=1
	p=obj.food.price
	obj.price=p*obj.quantity
	obj.save()
	return redirect(menu)

def minus_item(request,pk):
	print('l')
	obj=Cart.objects.get(pk=pk)
	if obj.quantity>1:
		obj.quantity-=1
		p=obj.food.price
		obj.price=p*obj.quantity
		obj.save()
	return redirect(menu)

def my_account(request):
	data=Customer.objects.get(customer=request.user)
	return render(request,'app/account.html',{'data':data})

def fil_category(request,cat,canteen):
	
	category=Category.objects.get(id=cat)
	cant=User.objects.get(id=canteen)
	obj=Menu.objects.filter(food_categoary=category,canteen=cant)
	cat=Category.objects.all()
	canteen=User.objects.filter(is_restaurant=True)

	if request.user.is_authenticated:
		cart=Cart.objects.filter(customer=request.user)
		no_of_items=len(list(cart))
		print(no_of_items,'no of items')
		total=Cart.objects.aggregate(Sum('price'))
		return render(request,'app/menu.html',{'menu':obj,'cart':cart,'cat':cat,'total':total,'items':no_of_items,'canteen':canteen})
	return render(request,'app/menu.html',{'menu':obj,'cat':cat,'canteen':canteen})

def my_order(request):
	cart=Cart.objects.filter(customer=request.user)
	canteen=Cart.objects.filter(customer=request.user).values('canteen').distinct()
	print(canteen)
	datetime=request.POST.get('date_time')
	total=0
	orderid=''
	for i in canteen:
		price=Cart.objects.filter(customer=request.user,canteen=i['canteen']).aggregate(Sum('price'))
		
		cant=User.objects.get(id=i['canteen'])
		ord=Orders.objects.create(total_price=price['price__sum'],ordered_by=request.user,time=datetime,ordered_to=cant)
		total+=int(price['price__sum'])
		if len(orderid)==0:
			orderid+=str(ord.id)
		else:
			orderid=orderid+'-'+str(ord.id)
		print(orderid)

		cart=Cart.objects.filter(customer=request.user,canteen=i['canteen'])
		for i in cart:
			Myorder.objects.create(canteen_id=cant,menu=i.food,quant=i.quantity,order_id=ord)		
			i.delete()

	param_dict = {
 
        'MID': MID, #merchant id
        'ORDER_ID': orderid, 
        'TXN_AMOUNT': str(total),
        'CUST_ID': str(request.user.id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',#for testing
        'CHANNEL_ID': 'WEB',
        'MOBILE_NO':str(request.user.phone),
        'EMAIL':str(request.user.email),
        'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/'}
		
	param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MKEY)
	
	return render(request,'app/checkout.html',{'param_dict':param_dict})

def my_orders(request):
	order=Orders.objects.filter(ordered_by=request.user).order_by('-ordered_at').exclude(transaction_id='Failed')
	item=Myorder.objects.filter(order_id__ordered_by=request.user)
	print(order)
	return render(request,'app/my_orders.html',{'order':order,'item':item})

def ingredients(request,pk):
	obj=Menu.objects.get(pk=pk)
	ingre=Ingredients.objects.filter(food=obj)
	print(obj.description)
	return render(request,'app/ingredients.html',{'obj':obj,'ingredients':ingre})

def back(request):
	return redirect(menu)


def add_rating(request):
	rate=request.GET.get('rate')
	food=request.GET.get('food')
	food_item=Myorder.objects.get(id=food)
	food_item.cust_rating=rate
	food_item.save()

	menu=Menu.objects.get(id=food_item.menu.id)
	
	menu.total_rating=int(menu.total_rating)+int(rate)
	total=menu.total_rating
	menu.no_of_rating+=1
	no=menu.no_of_rating
	menu.save()
	menu.rating=total//no
	menu.save()


def home_search(request):
	if request.method=='POST':
		search=request.POST.get('search')

		obj=Menu.objects.filter(canteen__first_name__icontains=search)|Menu.objects.filter(food_name=search)|Menu.objects.filter(food_categoary__category_name__icontains=search)

		cat=Category.objects.all()
		canteen=User.objects.filter(is_restaurant=True)
		if len(list(obj))==0 or search=='':
			# obj='No item found'
			return render(request,'app/no_items.html')
		if request.user.is_authenticated:
			cart=Cart.objects.filter(customer=request.user)
			no_of_items=len(list(cart))
			print(no_of_items,'no of items')
			total=cart.aggregate(Sum('price'))
			return render(request,'app/menu.html',{'menu':obj,'cart':cart,'cat':cat,'total':total,'items':no_of_items,'canteen':canteen})
		else:
			return render(request,'app/menu.html',{'menu':obj,'cat':cat,'canteen':canteen,'items':0})
		print(obj)
	
	
	else:
		return redirect(menu)

def confirm_order(request):
	return render(request,'confirm_order.html')

def about_us(request):
	return render(request,'app/about_us.html')


def edit_profile(request):
	if request.method=='POST':
		form=EditProfile(request.POST,instance=request.user)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.phone=obj.username
			obj.save()
			return redirect(edit_profile)
	else:
		form=EditProfile(instance=request.user)
		form2=ProfileEdit(instance=request.user)
		return render(request,'app/edit_profile.html',{'form':form,'form2':form2})
