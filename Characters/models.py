import random
from math import ceil
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from django.http import request


class Raza(models.Model):
    nombre = models.CharField(max_length=100)
    bonificacion_fuerza = models.IntegerField(default=0)
    bonificacion_dextiridad = models.IntegerField(default=0)
    bonificacion_agilidad = models.IntegerField(default=0)
    bonificacion_vida = models.IntegerField(default=0)
    bonificacion_inteligencia = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='razas/', default='default.png')

    def __str__(self):
        return self.nombre

class Mapa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Puede ser 'alimento', 'arma', 'armadura', etc.
    puntos_recuperacion = models.IntegerField(default=0, null=True, blank=True)  # Usado solo para alimentos
    costo_oro = models.IntegerField(default=10, null=True, blank=True)
    daño_min = models.IntegerField(default=0, null=True, blank=True)
    daño_max = models.IntegerField(default=0, null=True, blank=True)
    armadura = models.IntegerField(default=0, null=True, blank=True)
    efecto = models.CharField(max_length=100, null=True, blank=True)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='objetos/', default='default.png')
    cantidad_disponible = models.IntegerField(default=10)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.tipo in ['Mano principal', 'Mano secundaria']:
            self.vendedor = Vendedor.objects.get_or_create(nombre='Vendedor de Armas')[0]
        elif self.tipo in ['Cabeza', 'Torso', 'Piernas', 'Guantes', 'Botas']:
            self.vendedor = Vendedor.objects.get_or_create(nombre='Vendedor de Armaduras')[0]
        elif self.tipo in ['Cuello', 'Anillo principal', 'Anillo secundario']:
            self.vendedor = Vendedor.objects.get_or_create(nombre='Vendedor de Joyas')[0]
        elif self.tipo == 'Alimento':
            self.vendedor = Vendedor.objects.get_or_create(nombre='Vendedor de Alimentos')[0]
        else:
            raise ValueError("Tipo de objeto no válido.")
        super().save(*args, **kwargs)

#Costo de mejora de Atributos
def calcular_costo_mejora(costo_actual):
    nuevo_costo = costo_actual * 1.10
    return ceil(nuevo_costo)

class Personaje(models.Model):

    #Datos principales
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank=True)
    nombre = models.CharField(max_length=100)
    poder = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    experiencia = models.IntegerField(default=0)
    daño_minimo = models.IntegerField(default=1)
    daño_maximo = models.IntegerField(default=1000)
    puntos_de_vida = models.IntegerField(default=100) #Vida maxima
    armadura = models.IntegerField(default=10)
    energia = models.IntegerField(default=12)
    raza = models.ForeignKey(Raza, on_delete=models.SET_NULL, null = True, blank=True)

    #Atributos
    fuerza = models.IntegerField(default=10)
    dextiridad = models.IntegerField(default=10)
    agilidad = models.IntegerField(default=10)
    vida = models.IntegerField(default=100)
    inteligencia = models.IntegerField(default=10)

    #Oro e inventario
    oro = models.IntegerField(default=100)

    # Slots de equipamiento
    mano_principal = models.ForeignKey(
        Objeto, related_name="equipado_mano_principal", on_delete=models.SET_NULL, null=True, blank=True
    )
    mano_secundaria = models.ForeignKey(
        Objeto, related_name="equipado_mano_secundaria", on_delete=models.SET_NULL, null=True, blank=True
    )
    cabeza = models.ForeignKey(
        Objeto, related_name="equipado_cabeza", on_delete=models.SET_NULL, null=True, blank=True
    )
    torso = models.ForeignKey(
        Objeto, related_name="equipado_torso", on_delete=models.SET_NULL, null=True, blank=True
    )
    piernas = models.ForeignKey(
        Objeto, related_name="equipado_piernas", on_delete=models.SET_NULL, null=True, blank=True
    )
    guantes = models.ForeignKey(
        Objeto, related_name="equipado_guantes", on_delete=models.SET_NULL, null=True, blank=True
    )
    botas = models.ForeignKey(
        Objeto, related_name="equipado_botas", on_delete=models.SET_NULL, null=True, blank=True
    )
    cuello = models.ForeignKey(
        Objeto, related_name="equipado_cuello", on_delete=models.SET_NULL, null=True, blank=True
    )
    anillo_principal = models.ForeignKey(
        Objeto, related_name="equipado_anillo_principal", on_delete=models.SET_NULL, null=True, blank=True
    )
    anillo_secundario = models.ForeignKey(
        Objeto, related_name="equipado_anillo_secundario", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Inventario
    inventario = models.OneToOneField('Inventario', on_delete=models.CASCADE, null=True, blank=True, related_name='heroe_inventario')

    #Costo de mejora de Atributos
    costo_mejora_fuerza = models.IntegerField(default=10)
    costo_mejora_dextiridad = models.IntegerField(default=10)
    costo_mejora_agilidad = models.IntegerField(default=8)
    costo_mejora_vida = models.IntegerField(default=5)
    costo_mejora_inteligencia = models.IntegerField(default=6)

    def __str__(self):
        return self.nombre

    # Calculo de daño de Personaje
    def calcular_atributos(self):
        # Inicializar atributos básicos del héroe sin considerar objetos equipados
        self.daño_minimo = 1 + (self.fuerza // 5)
        self.daño_maximo = 1 + (self.dextiridad // 3.5)
        self.armadura = 1 + (self.dextiridad // 2)

        # Lista de objetos equipados
        objetos_equipados = [
            self.mano_principal, self.mano_secundaria, self.cabeza, self.torso,
            self.piernas, self.guantes, self.botas, self.cuello,
            self.anillo_principal, self.anillo_secundario
        ]

        # Iterar sobre cada objeto equipado y ajustar los Atributos
        for objeto in objetos_equipados:
            if objeto:
                self.daño_minimo += objeto.daño_min
                self.daño_maximo += objeto.daño_max
                self.armadura += objeto.armadura

        # Asegurar que el daño máximo no sea menor que el daño mínimo
        if self.daño_maximo < self.daño_minimo:
            self.daño_maximo = self.daño_minimo

        self.puntos_de_vida = 10 + (self.vida // 1)

        #Calcular el ranking global
        self.ranking_global = self.nivel + self.experiencia + self.daño_maximo + self.armadura

    def save(self, *args, **kwargs):
        self.calcular_atributos()
        super().save(*args, **kwargs)

    def regenerar_energia(self):
        if self.energia < 12:
            self.energia += 1
            self.save()

class Nivel(models.Model):
    mapa = models.ForeignKey(Mapa, related_name='niveles', on_delete=models.CASCADE)
    numero = models.IntegerField()
    enemigos = models.ManyToManyField('Enemigo')
    jefe = models.BooleanField(default=False)

    def __str__(self):
        return f"Nivel {self.numero} - {self.mapa.nombre}"

class Enemigo(models.Model):
    nombre = models.CharField(max_length=100)
    puntos_de_vida = models.IntegerField(default=100)
    daño_minimo = models.IntegerField(default=10)
    daño_maximo = models.IntegerField(default=20)
    armadura = models.IntegerField(default=5)

    def __str__(self):
        return self.nombre

    def calcular_daño(self):
        return int(self.daño_minimo + (self.daño_maximo - self.daño_minimo) * random.random())

class Heroe(Personaje):

    ranking_global = models.IntegerField(default=0, editable=False)
    mapa_actual = models.ForeignKey(Mapa, null=True, blank=True, on_delete=models.SET_NULL)
    nivel_actual = models.IntegerField(default=1)
    progreso_nivel_mapa = models.IntegerField(default=1)
    vida_actual = models.IntegerField(default=100)

    def mejorar_atributo(self, atributo):
        if atributo == 'fuerza' and self.oro >= self.costo_mejora_fuerza:
            self.oro -= self.costo_mejora_fuerza
            self.fuerza += 1
            self.costo_mejora_fuerza = self.calcular_nuevo_costo(self.costo_mejora_fuerza)
            messages.success(request, "¡Fuerza aumentada!")
        elif atributo == 'dextiridad' and self.oro >= self.costo_mejora_dextiridad:
            self.oro -= self.costo_mejora_dextiridad
            self.dextiridad += 1
            self.costo_mejora_dextiridad = self.calcular_nuevo_costo(self.costo_mejora_dextiridad)
            messages.success(request, "¡Dextiridad aumentada!")
        elif atributo == 'agilidad' and self.oro >= self.costo_mejora_agilidad:
            self.oro -= self.costo_mejora_agilidad
            self.agilidad += 1
            self.costo_mejora_agilidad = self.calcular_nuevo_costo(self.costo_mejora_agilidad)
            messages.success(request, "¡Agilidad aumentada!")
        elif atributo == 'vida' and self.oro >= self.costo_mejora_vida:
            self.oro -= self.costo_mejora_vida
            self.vida += 10
            self.costo_mejora_vida = self.calcular_nuevo_costo(self.costo_mejora_vida)
            messages.success(request, "¡Vida aumentada!")
        elif atributo == 'inteligencia' and self.oro >= self.costo_mejora_inteligencia:
            self.oro -= self.costo_mejora_inteligencia
            self.inteligencia += 1
            self.costo_mejora_inteligencia = self.calcular_nuevo_costo(self.costo_mejora_inteligencia)
            messages.success(request, "¡Inteligencia aumentada!")
        else:
            raise ValueError("Oro insuficiente para mejorar el atributo o atributo desconocido.")
        self.save()

    def calcular_daño(self):
        daño_minimo = 1 + (self.fuerza // 5)
        daño_maximo = 1 + (self.dextiridad // 3.5)

        if self.mano_principal:
            daño_minimo += self.mano_principal.daño_min
            daño_maximo += self.mano_principal.daño_max

        if self.mano_secundaria:
            daño_minimo += self.mano_secundaria.daño_min
            daño_maximo += self.mano_secundaria.daño_max

        # Asegurar que daño_maximo no sea menor que daño_minimo
        if daño_maximo < daño_minimo:
            daño_maximo = daño_minimo

        return int(self.daño_minimo + (self.daño_maximo - self.daño_minimo) * random.random())

class Inventario(models.Model):
    heroe = models.OneToOneField(Heroe, on_delete=models.CASCADE, related_name='inventario_heroe')
    objeto = models.ManyToManyField(Objeto, through='InventarioObjeto')

class InventarioObjeto(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    objeto = models.ForeignKey(Objeto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, default="", editable=False)  # El tipo del objeto
    cantidad = models.IntegerField(default=1)
    equipado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Obtener el tipo del objeto asociado y asignarlo automáticamente
        self.tipo = self.objeto.tipo
        super().save(*args, **kwargs)

class Combate(models.Model):
    heroe = models.ForeignKey(Heroe, on_delete=models.CASCADE)
    enemigo = models.ForeignKey(Enemigo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.CharField(max_length=100)
    detalles_rondas = models.JSONField(default=list)

    def simular_combate(self):
        heroe = self.heroe
        enemigo = self.enemigo
        self.detalles_rondas = []

        if heroe.energia < 1:
            self.resultado = 'sin energía'
            self.save()
            return

        heroe.energia -= 1

        while heroe.vida_actual > 0 and enemigo.puntos_de_vida > 0:
            daño_heroe = max(0, int(heroe.calcular_daño()) - enemigo.armadura)
            enemigo.puntos_de_vida -= daño_heroe

            detalles_heroe = {
                "daño_realizado_heroe": daño_heroe,
                "vida_restante_enemigo": enemigo.puntos_de_vida
            }

            if enemigo.puntos_de_vida <= 0:
                self.resultado = 'victoria'
                heroe.progreso_nivel_mapa += 1
                heroe.experiencia += 10
                self.detalles_rondas.append(detalles_heroe)
                break

            daño_enemigo = max(0, int(enemigo.calcular_daño()) - heroe.armadura)
            heroe.vida_actual -= daño_enemigo
            if heroe.vida_actual < 0:
                heroe.vida_actual = 0

            detalles_enemigo = {
                "daño_realizado_enemigo": daño_enemigo,
                "vida_restante_heroe": heroe.vida_actual
            }

            self.detalles_rondas.append({**detalles_heroe, **detalles_enemigo})

            if heroe.vida_actual <= 0:
                self.resultado = 'derrota'
                break

        if heroe.vida_actual > heroe.puntos_de_vida:
            heroe.vida_actual = heroe.puntos_de_vida

        if heroe.experiencia >= heroe.nivel * 100:
            heroe.nivel += 1
            heroe.energia = 12
            heroe.vida_actual = heroe.puntos_de_vida  # Recupera toda su vida al subir de nivel

        heroe.save()
        self.save()
