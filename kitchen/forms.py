from django import forms


class PizzaSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by name'
            }
        ),
    )

class PizzaTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search by name'
            }
        ),
    )
