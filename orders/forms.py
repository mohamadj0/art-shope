from django import forms


class CartAddForms(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10)

class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=15)