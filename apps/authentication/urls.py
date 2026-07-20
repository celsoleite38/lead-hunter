from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.register_view, name="register"),
    path("verificar-email/", views.email_verification_sent_view, name="email_verification_sent"),
    path("verificar-email/<uidb64>/<token>/", views.email_verify_view, name="email_verify"),
    path("reenviar-ativacao/", views.resend_activation_view, name="resend_activation"),
    path("esqueci-senha/", views.password_reset_view, name="password_reset"),
    path("redefinir-senha/enviado/", views.password_reset_done_view, name="password_reset_done"),
    path("redefinir-senha/<uidb64>/<token>/", views.password_reset_confirm_view, name="password_reset_confirm"),
    path("perfil/", views.profile_view, name="profile"),
    path("senha/", views.password_change_view, name="password_change"),
]
