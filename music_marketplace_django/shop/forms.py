from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User, Product

class RegistrationForm(UserCreationForm):
    is_reseller = forms.BooleanField(label='Согласен стать перекупщиком', required=False)
    role_choices = [
        ('buyer', 'Покупатель'),
        ('musician', 'Музыкант'),
        ('label', 'Лейбл'),
        ('reseller', 'Перекупщик'),
    ]
    role = forms.ChoiceField(label='Роль', choices=role_choices, widget=forms.Select)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'is_reseller', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.is_reseller = self.cleaned_data['is_reseller']
        if 'profile_picture' in self.cleaned_data:
            user.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
            self.save_m2m()
        return user

class LoginForm(AuthenticationForm):
    pass

class ProductForm(forms.ModelForm):
    format = forms.ChoiceField(label='Формат', choices=Product.format_choices)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'genre', 'format', 'is_original']

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture') # Включаем profile_picture
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}), # Виджет для загрузки файла
        }