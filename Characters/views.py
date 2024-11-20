import random

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Personaje, Objeto, calcular_costo_mejora, Heroe, Inventario, Vendedor, Mapa, Combate, Nivel, InventarioObjeto


#FUNCIONES PARA INICIO DE SESION, REGISTRO O DESLOGEO
def cerrar_sesion(request):
    logout(request)

    return redirect('home')

def logearse(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                if not Personaje.objects.filter(user=usuario).exists():
                    return redirect('crear_heroe')
                messages.success(request, f"Bienvenido de nuevo {usuario.username}")
                return redirect('home')
            else:
                messages.error(request, "Usuario no válido")
        else:
            messages.error(request, "Algo está mal")

    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def index(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, HeroeForm

def registro(request):
    if request.method == "POST":
        user_form = SignUpForm(request.POST)
        heroe_form = HeroeForm(request.POST)
        if user_form.is_valid() and heroe_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            heroe = heroe_form.save(commit=False)
            heroe.user = user
            heroe.save()
            # Crear inventario para el héroe
            inventario = Inventario.objects.create(heroe=heroe)
            login(request, user)
            messages.success(request, "¡Felicitaciones! Tu cuenta ha sido creada con éxito")
            return redirect('home')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        user_form = SignUpForm()
        heroe_form = HeroeForm()

    return render(request, 'registro.html', {'user_form': user_form, 'heroe_form': heroe_form})

@login_required
def mejorar_atributo(request, atributo):
    heroe = get_object_or_404(Heroe, user=request.user)
    try:
        heroe.mejorar_atributo(atributo)
        messages.success(request, "Atributo Aumentado!")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('perfil_heroe')

@login_required
def perfil_heroe(request):
    heroe = Heroe.objects.get(user=request.user)
    return render(request, 'perfil_heroe.html', {'heroe': heroe})

@login_required
def mejorar_atributo(request, atributo):
    heroe = get_object_or_404(Personaje, user=request.user)
    if atributo == 'fuerza' and heroe.oro >= heroe.costo_mejora_fuerza:
        heroe.oro -= heroe.costo_mejora_fuerza
        heroe.fuerza += 1
        heroe.costo_mejora_fuerza = calcular_costo_mejora(heroe.costo_mejora_fuerza)
    elif atributo == 'dextiridad' and heroe.oro >= heroe.costo_mejora_dextiridad:
        heroe.oro -= heroe.costo_mejora_dextiridad
        heroe.dextiridad += 1
        heroe.costo_mejora_dextiridad = calcular_costo_mejora(heroe.costo_mejora_dextiridad)
    elif atributo == 'agilidad' and heroe.oro >= heroe.costo_mejora_agilidad:
        heroe.oro -= heroe.costo_mejora_agilidad
        heroe.agilidad += 1
        heroe.costo_mejora_agilidad = calcular_costo_mejora(heroe.costo_mejora_agilidad)
    elif atributo == 'vida' and heroe.oro >= heroe.costo_mejora_vida:
        heroe.oro -= heroe.costo_mejora_vida
        heroe.vida += 10
        heroe.costo_mejora_vida = calcular_costo_mejora(heroe.costo_mejora_vida)
    elif atributo == 'inteligencia' and heroe.oro >= heroe.costo_mejora_inteligencia:
        heroe.oro -= heroe.costo_mejora_inteligencia
        heroe.inteligencia += 1
        heroe.costo_mejora_inteligencia = calcular_costo_mejora(heroe.costo_mejora_inteligencia)
    else:
        return render(request, 'error.html', {'mensaje': 'Oro insuficiente para mejorar el atributo.'})

    heroe.save()
    return redirect('perfil_heroe')

@login_required
def crear_heroe(request):
    # Comprobar si el usuario ya tiene un héroe
    if Heroe.objects.filter(user=request.user).exists():
        return redirect('home')  # Redirigir al home si ya tiene un héroe

    if request.method == "POST":
        heroe_form = HeroeForm(request.POST)
        if heroe_form.is_valid():
            heroe = heroe_form.save(commit=False)
            heroe.user = request.user
            heroe.save()
            inventario = Inventario.objects.create(heroe=heroe)
            heroe.inventario = inventario #####################ME QUEDE ACA
            messages.success(request, "Bien ya creaste a tu heroe!")
            return redirect('home')
    else:
        heroe_form = HeroeForm()

    return render(request, 'crear_heroe.html', {'heroe_form': heroe_form})


@login_required
def mostrar_inventario(request):
    heroe = get_object_or_404(Heroe, user=request.user)
    inventario = get_object_or_404(Inventario, heroe=heroe)

    # Obtener todos los objetos agrupados por tipo
    armas = Objeto.objects.filter(tipo__in=['Mano principal', 'Mano Secundaria'])
    armaduras = Objeto.objects.filter(tipo__in=['Cabeza', 'Torso', 'Piernas', 'Guantes', 'Botas'])
    joyas = Objeto.objects.filter(tipo__in=['Cuello', 'Anillo principal', 'Anillo secundario'])
    alimentos = Objeto.objects.filter(tipo='Alimento')

    # Obtener los objetos en el inventario del héroe
    inventario_objetos = InventarioObjeto.objects.filter(inventario=inventario)

    context = {
        'heroe': heroe,
        'inventario': inventario,
        'armas': armas,  # Pasamos las armas
        'armaduras': armaduras,  # Pasamos las armaduras
        'joyas': joyas,  # Pasamos las joyas
        'alimentos': alimentos,  # Pasamos los alimentos
        'inventario_objetos': inventario_objetos,
    }
    return render(request, 'inventario.html', context)

@login_required
def equipar_objetos(request, objeto_id, tipo):
    # Obtener el héroe del usuario
    personaje = get_object_or_404(Heroe, user=request.user)
    inventario = personaje.inventario
    objeto = get_object_or_404(Objeto, id=objeto_id)

    # Verificar si el objeto está en el inventario y disponible
    inventario_objeto = InventarioObjeto.objects.filter(inventario=inventario, objeto=objeto).first()
    if not inventario_objeto or inventario_objeto.cantidad <= 0:
        messages.error(request, "El objeto no está disponible en tu inventario.")
        return redirect('mostrar_inventario')

    # Mapear el tipo de objeto al slot correspondiente
    tipo_a_slot = {
        'Cabeza': 'cabeza',
        'Torso': 'torso',
        'Piernas': 'piernas',
        'Mano principal': 'mano_principal',
        'Mano secundaria': 'mano_secundaria',
        'Cuello': 'cuello',
        'Anillo principal': 'anillo_principal',
        'Anillo secundario': 'anillo_secundario',
        'Botas': 'botas',
        'Guantes': 'guantes',
    }

    slot = tipo_a_slot.get(tipo)  # Usa el tipo recibido de la URL
    if not slot:
        messages.error(request, "No puedes equipar este tipo de objeto.")
        return redirect('mostrar_inventario')

    # Verificar si el slot ya está ocupado
    if getattr(personaje, slot):
        # Desequipar el objeto actualmente equipado en ese slot
        objeto_actual = getattr(personaje, slot)
        inventario_objeto_actual = InventarioObjeto.objects.filter(inventario=inventario, objeto=objeto_actual).first()
        if inventario_objeto_actual:
            inventario_objeto_actual.cantidad += 1
            inventario_objeto_actual.equipado = False
            inventario_objeto_actual.save()

    # Equipar el nuevo objeto
    setattr(personaje, slot, objeto)  # Asignar el objeto al slot
    personaje.save()

    # Actualizar el inventario
    inventario_objeto.cantidad -= 1
    if inventario_objeto.cantidad <= 0:
        inventario_objeto.delete()
    else:
        inventario_objeto.equipado = True
        inventario_objeto.save()

    messages.success(request, f"Has equipado {objeto.nombre} en {slot.replace('_', ' ')}.")
    return redirect('mostrar_inventario')

@login_required
def desequipar_objetos(request, objeto_id, tipo):
    # Obtener el personaje del usuario
    personaje = get_object_or_404(Personaje, user=request.user)
    inventario = personaje.inventario  # Inventario asociado al personaje
    objeto = get_object_or_404(Objeto, id=objeto_id)

    # Mapear el tipo de objeto al slot correspondiente
    tipo_a_slot = {
        'Cabeza': 'cabeza',
        'Torso': 'torso',
        'Piernas': 'piernas',
        'Mano principal': 'mano_principal',
        'Mano secundaria': 'mano_secundaria',
        'Cuello': 'cuello',
        'Anillo principal': 'anillo_principal',
        'Anillo secundario': 'anillo_secundario',
        'Botas': 'botas',
        'Guantes': 'guantes',
    }

    slot = tipo_a_slot.get(tipo)
    if not slot:
        messages.error(request, "No puedes desequipar este tipo de objeto.")
        return redirect('mostrar_inventario')

    # Verificar si el objeto está en el slot del personaje
    objeto_actual = getattr(personaje, slot)
    if objeto_actual != objeto:
        messages.error(request, "Este objeto no está equipado en ese slot.")
        return redirect('mostrar_inventario')

    # Desequipar el objeto
    setattr(personaje, slot, None)  # Remover el objeto del slot
    personaje.save()

    # Agregar el objeto al inventario
    inventario_objeto, created = InventarioObjeto.objects.get_or_create(inventario=inventario, objeto=objeto)
    inventario_objeto.cantidad += 1
    inventario_objeto.equipado = False
    inventario_objeto.save()

    messages.success(request, f"Has desequipado {objeto.nombre}.")
    return redirect('mostrar_inventario')


@login_required
def vendedor_objetos(request, tipo_vendedor):
    heroe = Heroe.objects.get(user=request.user)

    vendedor_nombre = f"Vendedor de {tipo_vendedor.capitalize()}"
    vendedor = Vendedor.objects.filter(nombre=vendedor_nombre).first()

    if not vendedor:
        messages.error(request, f"No se encontró un vendedor para {tipo_vendedor}.")
        return redirect('home')

    objetos = Objeto.objects.filter(tipo=tipo_vendedor, vendedor=vendedor, cantidad_disponible__gt=0)

    return render(request, 'vendedor.html', {
        'heroe': heroe,
        'objetos': objetos,
        'tipo_vendedor': tipo_vendedor,
        'vendedor': vendedor
    })


@login_required
def comprar_objeto(request, objeto_id):
    heroe = Heroe.objects.get(user=request.user)
    objeto = get_object_or_404(Objeto, id=objeto_id)

    if objeto.cantidad_disponible <= 0:
        messages.error(request, 'Este objeto ya no está disponible.')
        return redirect('vendedor_objetos', tipo=objeto.tipo)

    if heroe.oro >= objeto.costo_oro:
        heroe.oro -= objeto.costo_oro
        objeto.cantidad_disponible -= 1
        objeto.save()

        inventario, created = Inventario.objects.get_or_create(heroe=heroe)
        inventario_objeto, created = InventarioObjeto.objects.get_or_create(inventario=inventario, objeto=objeto)
        inventario_objeto.cantidad += 1
        inventario_objeto.save()

        heroe.save()
        messages.success(request, f'Has comprado {objeto.nombre}.')
    else:
        messages.error(request, 'No tienes suficiente oro para comprar este objeto.')

    return redirect('vendedor_objetos', tipo=objeto.tipo)

"""
@login_required
def vendedor_alimentos(request):
    heroe = Heroe.objects.get(user=request.user)
    alimentos = Alimento.objects.filter(cantidad_disponible__gt=0)
    return render(request, 'vendedor_alimento.html', {'heroe': heroe, 'alimentos': alimentos})"""

def ranking_global(request):
    heroes = Heroe.objects.all().order_by('-ranking_global')
    user_heroe = None
    user_posicion = None

    if request.user.is_authenticated:
        user_heroe = Heroe.objects.get(user=request.user)
        user_posicion = list(heroes).index(user_heroe) + 1

    return render(request, 'ranking_global.html', {
        'heroes': heroes,
        'user_heroe': user_heroe,
        'user_posicion': user_posicion
    })

@login_required
def seleccionar_mapa(request):
    mapas = Mapa.objects.all()
    return render(request, 'seleccionar_mapa.html', {'mapas': mapas})

@login_required
def seleccionar_nivel(request, mapa_id):
    mapa = get_object_or_404(Mapa, id=mapa_id)
    heroe = Heroe.objects.get(user=request.user)
    niveles = mapa.niveles.filter(numero__lte=heroe.progreso_nivel_mapa)
    return render(request, 'seleccionar_nivel.html', {'mapa': mapa, 'niveles': niveles})


@login_required
def combatir_enemigo(request, nivel_id):
    # Obtiene el nivel especificado por 'nivel_id'. Si no se encuentra, devuelve un error 404.
    nivel = get_object_or_404(Nivel, id=nivel_id)

    # Obtiene todos los enemigos relacionados con el nivel.
    enemigos = nivel.enemigos.all()

    # Selecciona un enemigo al azar de la lista de enemigos del nivel.
    enemigo = random.choice(enemigos)

    # Obtiene el héroe asociado con el usuario que está haciendo la solicitud.
    heroe = Heroe.objects.get(user=request.user)

    # Crea un objeto de Combate y lo guarda en la base de datos.
    combate = Combate.objects.create(heroe=heroe, enemigo=enemigo)

    # Simula el combate entre el héroe y el enemigo.
    combate.simular_combate()

    # Devuelve una página con el resultado del combate.
    return render(request, 'resultado_combate.html', {'combate': combate, 'heroe': heroe, 'enemigo': enemigo})


@login_required
def consumir_objeto(request, objeto_id):
    heroe = Heroe.objects.get(user=request.user)
    inventario = Inventario.objects.get(heroe=heroe)
    inventario_objeto = get_object_or_404(InventarioObjeto, inventario=inventario, objeto__id=objeto_id)

    if inventario_objeto.objeto.tipo == 'alimento':
        heroe.vida_actual += inventario_objeto.objeto.puntos_recuperacion
        if heroe.vida_actual > heroe.puntos_de_vida:
            heroe.vida_actual = heroe.puntos_de_vida

        inventario_objeto.cantidad -= 1
        if inventario_objeto.cantidad <= 0:
            inventario_objeto.delete()
        else:
            inventario_objeto.save()

        heroe.save()
        messages.success(request,
                         f'Has consumido {inventario_objeto.objeto.nombre} y recuperado {inventario_objeto.objeto.puntos_recuperacion} puntos de vida.')

    return redirect('perfil_heroe')