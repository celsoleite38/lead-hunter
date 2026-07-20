from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sua senha",
            }
        ),
    )


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nome",
            }
        ),
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sobrenome",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
            }
        ),
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "(11) 99999-9999",
            }
        ),
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Crie uma senha",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme a senha",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=80,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )
    avatar = forms.FileField(
        label="Foto",
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "avatar"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email


class PasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(
        label="Senha atual",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Senha atual",
            }
        ),
    )
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nova senha",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme a nova senha",
            }
        ),
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
                "autofocus": True,
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError(
                "Nenhuma conta encontrada com este e-mail."
            )
        return email


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nova senha",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme a nova senha",
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2


class ResendActivationForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
                "autofocus": True,
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email, is_active=False, email_verified=False).exists():
            raise forms.ValidationError(
                "Nenhuma conta pendente de ativação encontrada com este e-mail."
            )
        return email
