from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            'type': 'text',
            'class':'form-control',
            'placeholder':'First Name',
            'aria-label':'First Name',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["last_name"].widget.attrs.update({
            'type': 'text',
            'class':'form-control',
            'placeholder':'Last Name',
            'aria-label':'Last Name',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["username"].widget.attrs.update({
            'type': 'text',
            'class':'form-control',
            'placeholder':'Username',
            'aria-label':'Username',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["email"].widget.attrs.update({
            'type': 'email',
            'class':'form-control',
            'placeholder':'Email',
            'aria-label':'Email',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["password1"].widget.attrs.update({
            'type': 'password',
            'class':'form-control',
            'placeholder':'Password',
            'aria-label':'Password',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["password2"].widget.attrs.update({
            'type': 'password',
            'class':'form-control',
            'placeholder':'Confirm Password',
            'aria-label':'Confirm Password',
            'aria-describedby':'addon-wrapping'
        })

    
    email = forms.EmailField() # required=true is by default which means - email has to be entered

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
class UserUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            'type': 'text',
            'class':'form-control',
            'placeholder':'First Name',
            'aria-label':'First Name',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["last_name"].widget.attrs.update({
            'type': 'text',
            'class':'form-control',
            'placeholder':'Last Name',
            'aria-label':'Last Name',
            'aria-describedby':'addon-wrapping'
        })
        self.fields["email"].widget.attrs.update({
            'type': 'email',
            'class':'form-control',
            'placeholder':'Email',
            'aria-label':'Email',
            'aria-describedby':'addon-wrapping'
        })
    
    email = forms.EmailField() # required=true is by default which means - email has to be entered

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        