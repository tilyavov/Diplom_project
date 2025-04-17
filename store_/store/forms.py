from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Import get_user_model
from .models import Product, UserProfile

User = get_user_model()  # Get the User model

class ExtendedUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        label="Роль"
    )
    is_reseller = forms.BooleanField(
        label="Я перекупщик",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = User  # Use the User model
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']
        is_reseller = self.cleaned_data['is_reseller']
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=role, is_reseller=is_reseller)
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'genre', 'seller_type', 'is_original']