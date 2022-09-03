from django import forms


class CartAddForms(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10)