from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0,
        initial=1
    )

    override = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )