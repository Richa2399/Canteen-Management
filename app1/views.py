from django.shortcuts import render,redirect
from . forms import *
from . models import *
from app.models import CanteenProfile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
User=get_user_model()
from django.db.models import Sum
from django.db.models import Count
import datetime
import requests
import json


MID='eEBWPB26257464899048'
MKEY='&aNqcrbno!fZ1RIw'
# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
from paytm import Checksum

# Create your views here.
def indexPage(request):
	
	new=Orders.objects.filter(ordered_to=request.user,status='Pending').count()
	pending=Orders.objects.filter(ordered_to=request.user,status='Accept').count()
	completed=Orders.objects.filter(ordered_to=request.user,status='Complete').count()
	image=Menu.objects.filter(canteen=request.user)[:6]
	print(datetime.date.today())
	today = datetime.date.today()
	today_min=datetime.datetime.combine(datetime.date.today(),datetime.time.min)
	today_max=datetime.datetime.combine(datetime.date.today(),datetime.time.max)

	#date_created__year=today.year, date_created__month=today.month, date_created__day=today.day
	sale=Orders.objects.filter(ordered_to=request.user,status='Complete', ordered_at__range=(today_min,today_max)).aggregate(Sum('total_price'))
	sale_total=Orders.objects.filter(ordered_to=request.user,status='Complete', ordered_at__range=(today_min,today_max)).count()
	#print(sale)


	canteen=CanteenProfile.objects.get(canteen=request.user)
	ord=Myorder.objects.filter(canteen_id=request.user).values('menu__rating','menu__food_name').annotate(score=Count('menu__food_name')).order_by('score')
	print(ord)

	customer=Orders.objects.filter(ordered_to=request.user).values('ordered_by__first_name','ordered_by__last_name','ordered_by__email').annotate(score=Count('ordered_by__email')).order_by('score')
	print(customer )
	return render(request,'app1/index.html',{'customer':customer,'ord':ord,'new':new,'in_process':pending,'completed':completed,'image':image,'sale':sale,'sale_total':sale_total,'canteen':canteen})


def categoryPage(request):
	if request.method=='POST':
		form=CategoryForm(request.POST)
		if form.is_valid():
			form=form.save(commit=False)
			form.canteen_name=request.user
			form.save()
			return redirect(manage_category)
	else:
		form=CategoryForm()
		return render(request,'app1/foodcategory.html',{'form':form})

def menuPage(request):
	if request.method=='POST':
		form=MenuForm(request.POST,request.FILES,request=request)
		if form.is_valid():
			form=form.save(commit=False)
			form.canteen=request.user
			form.save()

			return redirect(add_ingredient,form.id)
		else:
			form=MenuForm(request.POST,request.FILES,request=request)
			return render(request,'app1/fooditem.html',{'form':form})

	else:
		form=MenuForm(request=request)
		return render(request,'app1/fooditem.html',{'form':form})

def add_ingredient(request,id):
	if request.method=='POST':
		form=IngredientForm(request.POST)

		if form.is_valid():
			form=form.save(commit=False)	
			menu=Menu.objects.get(id=id)
			form.food=menu
			form.save()
			return redirect(add_ingredient,id)	

	else:
		menu=Menu.objects.get(id=id)
		ingredient=Ingredients.objects.filter(food=menu)
		form=IngredientForm()

		return render(request,'app1/add_ingredient.html',{'ingredient':ingredient,'form':form})



def manage_category(request):
	data=Category.objects.filter(canteen_name=request.user)
	return render(request,'app1/managecategory.html',{'data':data})

def manage_menu(request):
	data=Menu.objects.filter(canteen=request.user)
	return render(request,'app1/managemenu.html',{'data':data})

def cat_del(request,pk):
	obj=Category.objects.get(pk=pk)
	obj.delete()
	return redirect(manage_category)

def menu_del(request,pk):
	obj=Menu.objects.get(pk=pk)
	obj.delete()
	return redirect(manage_menu)

def cat_edit(request,pk):
	if request.method=='POST':
		obj=Category.objects.get(pk=pk)
		form=CategoryForm(request.POST,instance=obj)
		if form.is_valid():
			form.save()
			return redirect(manage_menu)
	else:
		obj=Category.objects.get(pk=pk)
		form=CategoryForm(instance=obj)
		return render(request,'app1/foodcategory.html',{'form':form})


def menu_edit(request,pk):
	if request.method=='POST':
		obj=Menu.objects.get(pk=pk)
		form=MenuForm(request.POST,instance=obj,request=request)
		if form.is_valid():
			form.save()
			#messages.success(request,'Edit successfull')
			return redirect(manage_category)
	else:
		obj=Menu.objects.get(pk=pk)
		form=MenuForm(instance=obj,request=request)
		return render(request,'app1/fooditem.html',{'form':form})


def can_login(request):

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

					
					return redirect('index')
			else:
				return render(request,'app1/canlogin.html',{'message':'Invalid email or password'})

	return render(request,'app1/canlogin.html')



def canteenregisterpage(request):
	if request.method=='POST':
		name=request.POST.get('name')
		Phone=request.POST.get('phone')
		# enrollment=request.POST.get('enrollment')
		email =request.POST.get('email')
		pasword=request.POST.get('pasword2')
		print(email,'email')
		user_obj=User.objects.create_user(username=Phone,password=pasword,email=email,is_restaurant=True,is_student=False,is_staff=False,first_name=name,phone=Phone)
		CanteenProfile.objects.create(canteen=user_obj)
		return redirect(can_login)
	else:
		return render(request,'app1/canteenregister.html')

def logout_user(request):
	logout(request)
	return redirect(can_login)

def pending_order(request):
	return render(request,'app1/pending_order.html')

def new_order(request):
	order=Orders.objects.filter(status='Pending',ordered_to=request.user)
	item=Myorder.objects.filter(status="Pending",canteen_id=request.user)
	#print(customer,'jhjhj')
	return render(request,'app1/new_order2.html',{'order':order,'item':item})

def completed_order(request):
	return render(request,'app1/completed_order.html')



def accept_order(request,pk):
	order=Orders.objects.get(pk=pk)
	order.status='Accept'
	order.save()

	items=Myorder.objects.filter(order_id=order,canteen_id=request.user)
	for i in items:
		i.status='Accept'
		i.save()
	return redirect(new_order)	

def cancel_order(request,pk):
	order=Orders.objects.get(pk=pk)
	order.status='Cancel'
	order.save()

	items=Myorder.objects.filter(order_id=order,canteen_id=request.user)
	for i in items:
		i.status='Cancel'
		i.save()

	# body parameters
	paytmParams = dict()
	paytmParams["body"] = {

	# Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	"mid" :MID,

	# This has fixed value for refund transaction
	"txnType" : "REFUND",

	# Enter your order id for which refund needs to be initiated
	"orderId" : str(order.id),

	# Enter transaction id received from Paytm for respective successful order
	"txnId" : str(order.transaction_id),

	# Enter numeric or alphanumeric unique refund id
	"refId" : str(order.id),

	# Enter amount that needs to be refunded, this must be numeric
	"refundAmount" : str(order.total_price)
	}
	checksum = Checksum.generate_checksum_by_str(json.dumps(paytmParams["body"]), MKEY)
	# head parameters
	paytmParams["head"] = {

	# This is used when you have two different merchant keys. In case you have only one please put - C11
	"clientId" :str(order.ordered_by.id),

	# put generated checksum value here
	"signature" : checksum
	}
	post_data = json.dumps(paytmParams)
	url = "https://securegw-stage.paytm.in/refund/apply"
	response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
	#return render(request,'app1/refund.html',{'param_dict':paytmParams})
	post_data = json.dumps(paytmParams)  
	print(post_data)
	order=Orders.objects.get(pk=pk)
	order.payment_status='Refund'
	order.save()
	'''
	Refund.objects.create(refund_amount=order.total_price,txnId=post_data['body']['resultInfo']['txnId'],order=order,refundId=post_data['body']['resultInfo']['refundId'])
	response['refundId']
	'''
	return redirect(new_order)


def processing_order(request):
	order=Orders.objects.filter(status='Accept',ordered_to=request.user)
	item=Myorder.objects.filter(status="Accept",canteen_id=request.user)
	#print(customer,'jhjhj')
	return render(request,'app1/in_process_order.html',{'order':order,'item':item})



def complete_order(request,pk):
	order=Orders.objects.get(pk=pk)
	order.status='Complete'
	order.save()

	items=Myorder.objects.filter(order_id=order,canteen_id=request.user)
	for i in items:
		i.status='Complete'
		i.save()
	return redirect(completed_order)

def completed_order(request):
	order=Orders.objects.filter(status='Complete',ordered_to=request.user)
	item=Myorder.objects.filter(status="Complete",canteen_id=request.user)
	#print(customer,'jhjhj')
	return render(request,'app1/completed_order.html',{'order':order,'item':item})





def quality(request):
	return render(request,'app1/quality.html')


def sale_report(request):
	if request.method=='POST':
		yearmonth=request.POST.get('yearmonth')
		year,month=yearmonth.split('-')
		sale_data=Orders.objects.filter(ordered_to=request.user,payment_status='Paid',status='Complete',ordered_at__month=month,ordered_at__year=year).values('ordered_at').order_by('ordered_at').annotate(sum=Sum('total_price'))
		sale=Orders.objects.filter(ordered_to=request.user,payment_status='Paid',status='Complete',ordered_at__month=month,ordered_at__year=year).aggregate(Sum('total_price'))
		print(sale)
		return render(request,'app1/sale_report.html',{'sale_data':sale_data,'sale':sale})
	else:
		today = datetime.date.today()
		sale_data=Orders.objects.filter(status='Complete',ordered_to=request.user,payment_status='Paid',ordered_at__month=today.month,ordered_at__year=today.year).values('ordered_at').order_by('ordered_at').annotate(sum=Sum('total_price'))
		sale=Orders.objects.filter(status='Complete',ordered_to=request.user,payment_status='Paid',ordered_at__month=today.month,ordered_at__year=today.year).aggregate(Sum('total_price'))
		print(sale_data)
		return render(request,'app1/sale_report.html',{'sale_data':sale_data,'sale':sale})

def can_account(request):
	if request.method=="POST":
		form=form=EditProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			return redirect(can_account)
	form=EditProfileForm(instance=request.user)
	return render(request,'app1/can_account.html',{'form':form})









