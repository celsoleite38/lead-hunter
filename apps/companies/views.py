from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompanyForm
from .models import Company


@login_required
def empresa_list_view(request):
    companies = Company.objects.filter(owner=request.user)
    can_add = companies.count() < request.user.max_companies
    return render(request, "companies/empresa_list.html", {
        "companies": companies,
        "can_add": can_add,
    })


@login_required
def empresa_create_view(request):
    companies = Company.objects.filter(owner=request.user)

    if companies.count() >= request.user.max_companies:
        messages.warning(request, "Você já atingiu o limite de empresas. Consulte o administrador.")
        return redirect("empresa")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, "Empresa criada com sucesso!")
            return redirect("empresa")
    else:
        form = CompanyForm()

    return render(request, "companies/empresa_form.html", {"form": form})


@login_required
def empresa_edit_view(request, slug):
    company = get_object_or_404(Company, slug=slug, owner=request.user)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa atualizada com sucesso!")
            return redirect("empresa")
    else:
        form = CompanyForm(instance=company)

    return render(request, "companies/empresa_form.html", {
        "form": form,
        "company": company,
    })
