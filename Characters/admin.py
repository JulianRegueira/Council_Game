from django.contrib import admin
from .models import Raza, Personaje, Objeto, Heroe, Vendedor, Mapa, Enemigo, Nivel, Inventario, InventarioObjeto

admin.site.register(Mapa)
admin.site.register(Nivel)
admin.site.register(Enemigo)
"""
admin.site.register(Subasta)"""

# Inline para mostrar los objetos relacionados con el inventario
class InventarioObjetoInline(admin.TabularInline):
    model = InventarioObjeto
    extra = 0  # No mostrar filas vacías por defecto
    fields = ['objeto', 'cantidad']  # Campos que se mostrarán en el inline
    readonly_fields = ['objeto']  # Hacer que el campo "objeto" no sea editable desde aquí

# Personalización del admin de Inventario
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['heroe', 'mostrar_objetos']  # Campos que se muestran en la lista
    search_fields = ['heroe__nombre']  # Habilitar búsqueda por el héroe
    inlines = [InventarioObjetoInline]  # Añadir el inline para InventarioObjeto

    def mostrar_objetos(self, obj):
        # Mostrar un resumen de los objetos en el inventario
        return ", ".join(f"{item.objeto.nombre} (x{item.cantidad})" for item in InventarioObjeto.objects.filter(inventario=obj))
    mostrar_objetos.short_description = "Objetos"

# Opcional: Registrar InventarioObjeto y Objeto para administrar directamente
@admin.register(InventarioObjeto)
class InventarioObjetoAdmin(admin.ModelAdmin):
    list_display = ['inventario', 'objeto', 'cantidad', 'tipo']
    list_filter = ['inventario__heroe', 'objeto']
    search_fields = ['inventario__heroe__nombre', 'objeto__nombre']

@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'vendedor', 'cantidad_disponible']
    search_fields = ['nombre', 'tipo']
    list_filter = ['tipo', 'vendedor']

# Inline para mostrar los objetos relacionados con un vendedor
class ObjetoInline(admin.TabularInline):
    model = Objeto
    extra = 0  # No mostrar filas vacías por defecto
    fields = ['nombre', 'tipo', 'costo_oro', 'cantidad_disponible']  # Campos que se mostrarán
    readonly_fields = ['nombre', 'tipo']  # Hacer campos no editables si corresponde
    can_delete = False  # Evitar borrar objetos desde aquí si es necesario

# Personalización del admin de Vendedor
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_objetos']  # Campos visibles en la lista
    search_fields = ['nombre']  # Permitir buscar por nombre del vendedor
    inlines = [ObjetoInline]  # Añadir los objetos como inline

    def cantidad_objetos(self, obj):
        # Contar la cantidad de objetos asociados al vendedor
        return Objeto.objects.filter(vendedor=obj).count()
    cantidad_objetos.short_description = "Cantidad de objetos"

# --- Inline para Personajes asociados a una raza ---
class PersonajeInline(admin.TabularInline):
    model = Personaje
    fields = ('nombre', 'nivel', 'experiencia', 'oro', 'fuerza', 'dextiridad', 'agilidad')
    extra = 0  # No añadir filas en blanco por defecto
    readonly_fields = ('nombre', 'nivel', 'experiencia', 'oro', 'fuerza', 'dextiridad', 'agilidad')

# --- Admin para Raza ---
@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'bonificacion_fuerza', 'bonificacion_dextiridad',
                    'bonificacion_agilidad', 'bonificacion_vida', 'bonificacion_inteligencia')
    search_fields = ('nombre',)
    inlines = [PersonajeInline]

# --- Admin para Personajes ---
@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'experiencia', 'poder', 'raza', 'oro', 'daño_minimo', 'daño_maximo', 'armadura')
    list_filter = ('nivel', 'raza')
    search_fields = ('nombre', 'raza__nombre')
    readonly_fields = ('calcular_atributos',)
    fieldsets = (
        ('Datos principales', {
            'fields': ('nombre', 'user', 'raza', 'nivel', 'experiencia', 'oro', 'energia')
        }),
        ('Atributos', {
            'fields': ('fuerza', 'dextiridad', 'agilidad', 'vida', 'inteligencia', 'armadura')
        }),
        ('Estadísticas de combate', {
            'fields': ('daño_minimo', 'daño_maximo', 'puntos_de_vida')
        }),
        ('Inventario', {
            'fields': ('mano_principal', 'mano_secundaria', 'cabeza', 'torso', 'piernas',
                       'guantes', 'botas', 'cuello', 'anillo_principal', 'anillo_secundario')
        }),
    )

# --- Admin para Héroes ---
@admin.register(Heroe)
class HeroeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel', 'ranking_global', 'vida_actual', 'mapa_actual', 'nivel_actual', 'progreso_nivel_mapa', 'oro')
    list_filter = ('mapa_actual', 'nivel')
    search_fields = ('nombre', 'mapa_actual__nombre')
    fieldsets = (
        ('Datos principales', {
            'fields': ('nombre', 'user', 'raza', 'nivel', 'experiencia', 'oro', 'energia')
        }),
        ('Atributos', {
            'fields': ('fuerza', 'dextiridad', 'agilidad', 'vida', 'inteligencia', 'armadura')
        }),
        ('Progreso', {
            'fields': ('mapa_actual', 'nivel_actual', 'progreso_nivel_mapa', 'vida_actual', 'ranking_global')
        }),
        ('Estadísticas de combate', {
            'fields': ('daño_minimo', 'daño_maximo', 'puntos_de_vida')
        }),
        ('Inventario', {
            'fields': ('mano_principal', 'mano_secundaria', 'cabeza', 'torso', 'piernas',
                       'guantes', 'botas', 'cuello', 'anillo_principal', 'anillo_secundario')
        }
         )
    )
