from django import forms
from .models import Order


class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone']

    def clean_coupon(self):
        if coupon := self.cleaned_data.get('coupon', None) and coupon.is_active:
            self.get_total_price -= coupon
            return coupon
        # now coupon is None
        return coupon