from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .forms import (
    LoginForm,
    PasswordChangeForm,
    PasswordResetRequestForm,
    RegistrationForm,
    ResendActivationForm,
    SetNewPasswordForm,
    UserProfileForm,
)
from .tokens import email_verification_token, password_reset_token
from .utils import send_password_reset_email, send_verification_email

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name}!")
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "authentication/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            return redirect("email_verification_sent")
    else:
        form = RegistrationForm()

    return render(request, "authentication/register.html", {"form": form})


def email_verification_sent_view(request):
    return render(request, "authentication/email_verification_sent.html")


def email_verify_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, "E-mail verificado com sucesso! Agora você pode fazer login.")
        return redirect("login")

    messages.error(request, "Link de verificação inválido ou expirado.")
    return redirect("login")


def resend_activation_view(request):
    if request.method == "POST":
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email, is_active=False, email_verified=False)
            send_verification_email(request, user)
            return redirect("email_verification_sent")
    else:
        form = ResendActivationForm()

    return render(request, "authentication/resend_activation.html", {"form": form})


def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()

    return render(request, "authentication/password_reset.html", {"form": form})


def password_reset_done_view(request):
    return render(request, "authentication/password_reset_done.html")


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not password_reset_token.check_token(user, token):
        messages.error(request, "Link de redefinição inválido ou expirado.")
        return redirect("password_reset")

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            messages.success(request, "Senha redefinida com sucesso! Agora você pode fazer login.")
            return redirect("login")
    else:
        form = SetNewPasswordForm()

    return render(request, "authentication/password_reset_confirm.html", {"form": form})


def password_reset_complete_view(request):
    return redirect("login")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "authentication/profile.html", {"form": form})


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "authentication/password_change.html", {"form": form})
