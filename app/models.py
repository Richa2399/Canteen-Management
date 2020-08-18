from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# AbstractBaseUser AbstractUser

class User(AbstractUser):
	
	is_staff=models.BooleanField(default=False)
	is_student=models.BooleanField(default=False)
	phone=models.BigIntegerField(default=91)
	is_restaurant=models.BooleanField(default=False)
	profile=models.ImageField(upload_to='profile/',default='pro.png')

	

	def __str__(self):
		return self.first_name+' '+self.last_name
	
		
class Customer(models.Model):
	customer=models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
	college_id=models.BigIntegerField(default=10000)
	idImage=models.ImageField(null=True,blank=True)

	def __str__(self):
		return self.customer.first_name

class CanteenProfile(models.Model):
	canteen=models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
	canteen_rating=models.CharField	(max_length=20,default='Not Assigned',choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))
	status=models.CharField(max_length=20,default='Active',choices=(('Block','Block'),('Active','Active')))

  