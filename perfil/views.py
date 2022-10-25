from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .models import Perfil
from django.core.validators import validate_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.urls import reverse
from django.core.cache import cache


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'perfil/cadastro.html')
    else:
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_confirma = request.POST.get('senha_confirma')
        telefone = request.POST.get('telefone')
        pais = request.POST.get('pais')
        foto = request.FILES['foto']

        # Verificando campos
        if not username or not email or not username or not senha or not senha_confirma or not nome or not pais\
                or not telefone or not foto:
            messages.error(request, 'Não deixe nenhum campo em branco')
            return render(request, 'perfil/cadastro.html')

        # Validador de email
        try:
            validate_email(email)
        except:
            messages.error(request, 'Email inválido')
            return render(request, 'perfil/cadastro.html')

        # Validador de senha
        if len(senha) < 8:
            messages.error(request, 'Senha precisa ter 8 caracteres ou mais.')
            return render(request, 'perfil/cadastro.html')

        if senha != senha_confirma:
            messages.error(request, 'Senhas não conferem.')
            return render(request, 'perfil/cadastro.html')

        # Verificação de usuario e email
        if Perfil.objects.filter(username=username).exists():
            messages.error(request, 'Usuario já existe.')
            return render(request, 'perfil/cadastro.html')

        if Perfil.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.  ')
            return render(request, 'perfil/cadastro.html')

        messages.success(request, 'Registrado com sucesso!')

        user = Perfil()
        user.nome = nome
        user.username = username
        user.telefone = telefone
        user.email = email
        user.password = senha
        user.pais = pais
        user.foto = foto
        user.save()

        return HttpResponseRedirect(reverse('index'))


def login(request):
    if request.method != 'POST':
        return render(request, 'perfil/login.html')

    username = request.POST.get('username')
    password = request.POST.get('senha')

    try:
        user = get_object_or_404(Perfil, username=username, senha=password)
        request.session['is_logged'] = True
    except:
        messages.error(request, 'Username ou senha inválida')
        return render(request, 'perfil/login.html')

    try:
        foto = user.foto.url
    except:
        foto = None

    if not user:
        return render(request, 'perfil/login.html')
    else:
        user_key = user.username
        request.session['user_key'] = user_key
        request.session['user'] = {
            'username': user.username,
            'nome': user.nome,
            'email': user.email,
            'telefone': user.telefone,
            'senha': user.senha,
            'pais': user.pais,
            'foto': foto,
        }

        return redirect('index')


def logout(request):
    try:
        del request.session['is_logged']
        cache.clear()
        return redirect('index')
    except:
        return redirect('index')