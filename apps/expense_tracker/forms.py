from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput
)

from django.contrib.auth.forms import ReadOnlyPasswordHashField

## Custom
from apps.expense_tracker.models import Category, Budget, Expense

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',  
                'placeholder': 'Enter Category Name',
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'This field is required'}


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']

        widgets = {
            'amount': forms.TextInput(attrs={
                'class': 'form-control',  
                'placeholder': 'Enter amount',
                'required': True,
            }),

            'category' : Select(attrs={
                'class': 'form-select js-choice', 
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)  ## Pop the user from kwargs
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         used_categories = Budget.objects.filter(owner=user).values_list('category', flat=True)
    #         self.fields['category'].queryset = Category.objects.exclude(id__in=used_categories)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  ## Pop the user from kwargs
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if user:
            ## Exclude categories already used by the user except the current category
            if instance:
                used_categories = Budget.objects.filter(owner=user).exclude(id=instance.id).values_list('category', flat=True)
            else:
                used_categories = Budget.objects.filter(owner=user).values_list('category', flat=True)
                
            self.fields['category'].queryset = Category.objects.exclude(id__in=used_categories)










# class AdminUpdateForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = [
#             'first_name', 'last_name', 'email', 'phone', 'image', 'gender', 'dob'
#         ]

#         widgets = {
#             'first_name' : TextInput( attrs={
#                     'class': 'form-control',  
#                     'placeholder': 'Enter First Name',
#                     'required': True,
#                 }),

#             'last_name' : TextInput( attrs={
#                     'class': 'form-control',  
#                     'placeholder': 'Enter Last Name',
#                     'required': True,
#                 }),

#             'email' : EmailInput(attrs={
#                     'class': 'form-control', 
#                     'placeholder': 'Enter Email',
#                     'required': True
#                 }),

#             'phone' : TextInput( attrs={
#                     'class': 'form-control', 
#                     'placeholder': 'Enter Phone Number',
#                     'required': True
#                 }),

#             'dob': forms.DateInput(
#                     format=('%Y-%m-%d'),
#                     attrs={'class': 'form-control',
#                         'placeholder': 'Select Birthdate',
#                         'type': 'date'
#                 }),

#             'image' : FileInput( attrs={
#                     # 'class': 'form-control show-img', 
#                     'class': 'form-control', 
#                     'accept' : 'image/jpeg image/png image/jpg',
#                     # 'style': 'border-style: dotted;',
#                 }),
            
#             'gender' : Select(attrs={
#                     'class': 'form-select js-choice', 
#                 }),
#         }





