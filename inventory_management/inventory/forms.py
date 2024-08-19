from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category']
        
class ItemFilterForm(forms.Form):
    name = forms.CharField(
        required=False, 
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Filter by name'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        label='Category'
    )
    min_quantity = forms.IntegerField(
        required=False, 
        label='Min Quantity'
    )
    max_quantity = forms.IntegerField(
        required=False, 
        label='Max Quantity'
    )
