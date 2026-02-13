from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import ShopUser
from django.contrib.auth.forms import AuthenticationForm


class UserValidationMixin():
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if ShopUser.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            return forms.ValidationError("شماره تلفن وجود دارد")
        if len(phone) > 11:
            return forms.ValidationError("شماره تلفن باید 11 رقم باشد")
        if not phone.startswith("09"):
            return forms.ValidationError("شماره تلفن باید با 09 شروع بشود")
        return phone


class ShopUserCreationForm(UserCreationForm, UserValidationMixin):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class ShopUserChangeForm(UserChangeForm, UserValidationMixin):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class RegisterForm(forms.ModelForm):

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'phone']

    password = forms.CharField(max_length=11, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(max_length=11, widget=forms.PasswordInput, label='repeated password')

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if ShopUser.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('!این شماره تلفن قبلا وارد شده')
        if len(phone) > 11:
            raise forms.ValidationError("شماره تلفن باید 11 رقم باشد")
        if not phone.startswith("09"):
            raise forms.ValidationError("شماره تلفن باید با 09 شروع بشود")
        return phone

    def clean_password2(self):
        if self.cleaned_data['password'] !=  self.cleaned_data['password2']:
            raise forms.ValidationError('رمزعبور مطابقت ندارد')
        return self.cleaned_data['password2']
    

class VerifictionPhoneForm(forms.Form):
    phone = forms.CharField(max_length=11, label="شماره تماس")