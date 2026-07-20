from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from .tokens import email_verification_token, password_reset_token


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    verify_url = request.build_absolute_uri(f"/verificar-email/{uid}/{token}/")

    print("\n" + "=" * 60)
    print(f"  LINK DE VERIFICACAO PARA: {user.email}")
    print(f"  {verify_url}")
    print("=" * 60 + "\n")

    subject = "Lead Hunter - Verifique seu e-mail"
    html_message = render_to_string("authentication/email/email_verify.html", {
        "user": user,
        "verify_url": verify_url,
    })
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "noreply@leadhunter.com.br",
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    reset_url = request.build_absolute_uri(f"/redefinir-senha/{uid}/{token}/")

    print("\n" + "=" * 60)
    print(f"  LINK DE REDEFINICAO DE SENHA PARA: {user.email}")
    print(f"  {reset_url}")
    print("=" * 60 + "\n")

    subject = "Lead Hunter - Redefinição de senha"
    html_message = render_to_string("authentication/email/email_password_reset.html", {
        "user": user,
        "reset_url": reset_url,
    })
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "noreply@leadhunter.com.br",
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
