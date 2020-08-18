from django import forms

from django.contrib.auth import get_user_model
from . models import *

class EditProfile(forms.ModelForm):
	#username=forms.CharFielld(attrs={'readonly':'readonly'})
	class Meta:
		model=get_user_model()
		fields=('email','first_name','last_name','username','profile')

		labels={
    		'username':'Phone no.',
    		'profile':'College Id'
    	}

class ProfileEdit(forms.ModelForm):
	class Meta:
		model=Customer
		fields=('college_id',)