from typing import List

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from decouple import config
from openpyxl import load_workbook

from license_db.handlers import save_to_disk
from license_db.utils import excel_columns, prepare_cell_value
from .models import License, ExcelEntry
from .forms import UploadFileForm


def auth(request, action='login'):
    if action == 'logout':
        logout(request)
        return redirect('license_db:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'login': {
            'prefix': config('LOGIN_PREFIX', default='DOMAIN\\'),
            'placeholder': config('LOGIN_PLACEHOLDER', default='Login'),
        },
        'access_denied': False,
    }

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('license_db:index')
        else:
            context['access_denied'] = True

    return render(request, 'license_db/auth.html', context)


def index(request):
    if request.user.is_anonymous:
        return redirect('license_db:auth')

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
    }

    lic_tree = {}
    for lic in License.objects.all():
        if lic.category.name not in lic_tree.keys():
            lic_tree[lic.category.name] = {}

        if lic.location.name not in lic_tree[lic.category.name].keys():
            lic_tree[lic.category.name][lic.location.name] = []

        lic_tree[lic.category.name][lic.location.name].append(lic)

    context['lic_tree'] = lic_tree

    return render(request, 'license_db/main.html', context)


def parse_excel(file_path: str) -> List[ExcelEntry]:
    entries = []

    wb = load_workbook(file_path)
    ws = wb.active

    rows = ws.rows
    next(rows)  # skip header row

    for row in rows:
        entry = ExcelEntry(
            name=prepare_cell_value(row, 'name'),
            category=prepare_cell_value(row, 'category'),
            location=prepare_cell_value(row, 'location'),
            lic_type=prepare_cell_value(row, 'lic_type'),
            quantity=prepare_cell_value(row, 'quantity'),
            expires=prepare_cell_value(row, 'expires'),
            comment=prepare_cell_value(row, 'comment'),
        )

        entries.append(entry)

    return entries


def show_preview(request, saved_file_info: dict):
    entries = parse_excel(saved_file_info['path'])

    print()

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        # 'form': form,
    }

    return render(request, 'license_db/preview.html', context)


def import_data(request):
    if request.user.is_anonymous:
        return redirect('license_db:auth')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            saved_file_info = save_to_disk(request.FILES['file'])

            preview_pressed = bool(request.POST.get('preview'))
            submit_pressed = bool(request.POST.get('submit'))

            if preview_pressed:
                show_preview(request, saved_file_info)

            if submit_pressed:
                submit_import(request, saved_file_info)
    else:
        form = UploadFileForm()

    context = {
        'logo': config('LOGO', default='My Logo'),
        'site_title': config('SITE_TITLE', default='My Site'),
        'form': form,
    }

    return render(request, 'license_db/import.html', context)
