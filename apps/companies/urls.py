from django.urls import path

from . import views

urlpatterns = [
    path("empresa/", views.empresa_list_view, name="empresa"),
    path("empresa/nova/", views.empresa_create_view, name="empresa_create"),
    path("empresa/<slug:slug>/editar/", views.empresa_edit_view, name="empresa_edit"),
]
