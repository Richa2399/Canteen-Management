from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()


class Category(models.Model):
	category_name=models.CharField(max_length=50,blank=True,null=True)
	canteen_name=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	
	def __str__(self):	
		return str(self.category_name)

	

class Menu(models.Model):
	food_categoary = models.ForeignKey(Category,on_delete=models.CASCADE)
	food_name = models.CharField(max_length=50,blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	food_image = models.ImageField(upload_to='food_image/')
	uploaded_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	price = models.IntegerField()
	canteen=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	total_rating=models.IntegerField(default=0)
	rating=models.FloatField(default=0)
	no_of_rating=models.IntegerField(default=0)
	
	def __str__(self):	
		return self.food_name


class Ingredients(models.Model):
	ingredient_name=models.CharField(max_length=20)
	ingredient_quantity=models.CharField(max_length=20)
	brand=models.CharField(max_length=30,null=True)
	food=models.ForeignKey(Menu,on_delete=models.CASCADE)


		
class Cart(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='custom')
	food=models.ForeignKey(Menu,on_delete=models.CASCADE)
	quantity=models.IntegerField(default=1)
	price = models.IntegerField(default=0)
	canteen=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='cantee')
	def __str__(self):	
		return self.customer.first_name


class Orders(models.Model):
	uploaded_at = models.DateTimeField(auto_now_add=True,null=True)	
	status=models.CharField(max_length=30,default='Pending',choices=(('Complete','Complete'),('Accept','Accept'),('Pending','Pending'),('Reject','Reject'),('Refund','Refund')))
	ordered_at=models.DateField(auto_now_add=True,null=True)
	total_price=models.IntegerField(null=True)
	ordered_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cust",null=True)
	time=models.CharField(max_length=20,null=True)
	ordered_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="canteen",null=True)
	payment_status=models.CharField(max_length=10,default='Pending',choices=(('Pending','Pending'),('Paid','Paid'),('Failed','Failed'),('COD','COD'),('Refund','Refund')))
	transaction_id=models.CharField(max_length=100,default='Failed')

class Myorder(models.Model):
	#customer_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cust")
	canteen_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cant")
	menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
	quant=models.IntegerField()
	
	order_id=models.ForeignKey(Orders,on_delete=models.CASCADE,null=True)
	status=models.CharField(max_length=30,default='Pending')
	cust_rating=models.IntegerField(default=0)
	#ordered_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cust",null=True)
	

class Refund(models.Model):
	refundId=models.CharField(max_length=30)
	order_id=models.ForeignKey(Orders,on_delete=models.CASCADE)
	refund_date=models.DateField(auto_now_add=True)
	refund_amount=models.IntegerField()
	txnId=models.CharField(max_length=30)