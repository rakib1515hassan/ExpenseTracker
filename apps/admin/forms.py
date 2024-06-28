from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from django.forms import (
    ModelForm, TextInput, Select, CheckboxInput, NumberInput, FileInput, SelectMultiple, Textarea,
    PasswordInput, EmailInput
)

from django.contrib.auth.forms import ReadOnlyPasswordHashField


class AdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Enter Password'}),
        label='Password'
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'image', 'gender', 'dob', 
            # 'is_active', 'is_verified', 'is_admin', 'is_superuser',
        ]

        widgets = {
            'first_name' : TextInput( attrs={
                    'class': 'form-control',  
                    'placeholder': 'Enter First Name',
                    'required': True,
                }),

            'last_name' : TextInput( attrs={
                    'class': 'form-control',  
                    'placeholder': 'Enter Last Name',
                    'required': True,
                }),

            'email' : EmailInput(attrs={
                    'class': 'form-control', 
                    'placeholder': 'Enter Email',
                    'required': True
                }),

            'phone' : TextInput( attrs={
                    'class': 'form-control', 
                    'placeholder': 'Enter Phone Number',
                    'required': True
                }),

            'dob': forms.DateInput(
                    format=('%Y-%m-%d'),
                    attrs={'class': 'form-control',
                        'placeholder': 'Select Birthdate',
                        'type': 'date'
                }),

            'image' : FileInput( attrs={
                    # 'class': 'form-control show-img', 
                    'class': 'form-control', 
                    'accept' : 'image/jpeg image/png image/jpg',
                    # 'style': 'border-style: dotted;',
                }),
            
            'gender' : Select(attrs={
                    'class': 'form-select js-choice', 
                }),

            ## Permissions
            # 'is_active'   : CheckboxInput(attrs={'class': 'form-check', 'type': 'checkbox', 'value': True}),

            # 'is_verified' : CheckboxInput(attrs={
            #         'class': 'form-check-input', 
            #         'type' : 'checkbox', 
            #         'value': True
            #     }),

            # 'is_superuser': CheckboxInput(attrs={'class': 'form-check'}),
            # 'is_admin'    : CheckboxInput(attrs={'class': 'form-check', 'type': 'checkbox', 'value': True, 'disabled':True}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        if password1 and len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return password2
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user








class AdminUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'image', 'gender', 'dob'
        ]

        widgets = {
            'first_name' : TextInput( attrs={
                    'class': 'form-control',  
                    'placeholder': 'Enter First Name',
                    'required': True,
                }),

            'last_name' : TextInput( attrs={
                    'class': 'form-control',  
                    'placeholder': 'Enter Last Name',
                    'required': True,
                }),

            'email' : EmailInput(attrs={
                    'class': 'form-control', 
                    'placeholder': 'Enter Email',
                    'required': True
                }),

            'phone' : TextInput( attrs={
                    'class': 'form-control', 
                    'placeholder': 'Enter Phone Number',
                    'required': True
                }),

            'dob': forms.DateInput(
                    format=('%Y-%m-%d'),
                    attrs={'class': 'form-control',
                        'placeholder': 'Select Birthdate',
                        'type': 'date'
                }),

            'image' : FileInput( attrs={
                    # 'class': 'form-control show-img', 
                    'class': 'form-control', 
                    'accept' : 'image/jpeg image/png image/jpg',
                    # 'style': 'border-style: dotted;',
                }),
            
            'gender' : Select(attrs={
                    'class': 'form-select js-choice', 
                }),
        }





