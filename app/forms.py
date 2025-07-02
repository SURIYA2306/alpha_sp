from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile ,Order

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Address'}),
        }
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
