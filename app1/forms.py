from .models import Category,Menu 
from django import forms
from . models import *
from django.contrib.auth import get_user_model
User=get_user_model()

class CategoryForm(forms.ModelForm):
	class Meta:
		model=Category
		fields=('category_name',)
	
class MenuForm(forms.ModelForm):
	class Meta:
		model=Menu
		fields=('food_categoary','food_name','description','food_image','price')


	def __init__(self,*args,**kwargs):
		self.request=kwargs.pop("request")
		super(MenuForm,self).__init__(*args,**kwargs)
		self.fields['food_categoary'].queryset=Category.objects.filter(canteen_name=self.request.user)


class IngredientForm(forms.ModelForm):
	class Meta:
		model=Ingredients
		fields=('ingredient_name','ingredient_quantity','brand')

class EditProfileForm(forms.ModelForm):
	
	class Meta:
		model=User
		fields=('first_name','username','profile','email')

		labels={'first_name':'Restaurant Name','username':'Phone No.','profile':'Profile Picture'}

