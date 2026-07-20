from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        label="Razão social",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Razão social"}
        ),
    )
    trade_name = forms.CharField(
        label="Nome fantasia",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nome fantasia"}
        ),
    )
    document = forms.CharField(
        label="CPF ou CNPJ",
        max_length=18,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "000.000.000-00 ou 00.000.000/0001-00"}
        ),
    )
    email = forms.EmailField(
        label="E-mail da empresa",
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "contato@empresa.com"}
        ),
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "(11) 99999-9999"}
        ),
    )

    class Meta:
        model = Company
        fields = ["name", "trade_name", "document", "email", "phone"]
