from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Asigna la vista de home a la raíz del sitio

    #LOGIN
    path('registro/', views.registro, name='registro'),
    path('login/', views.logearse, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('crear_heroe/', views.crear_heroe, name='crear_heroe'),

    #CHARACTER
    path('perfil/', views.perfil_heroe, name='perfil_heroe'),
    path('inventario/', views.mostrar_inventario, name='mostrar_inventario'),
    path('equipar/<int:objeto_id>/<str:tipo>', views.equipar_objetos, name='equipar_objetos'),
    path('desequipar_objeto/<int_objeto_id>/', views.desequipar_objetos, name='desequipar_objeto'),
    path('ranking_global/', views.ranking_global, name='ranking_global'),
    path('mejorar_atributo/<str:atributo>/', views.mejorar_atributo, name='mejorar_atributo'),

    #MAPA
    path('seleccionar_mapa/', views.seleccionar_mapa, name='seleccionar_mapa'),
    path('seleccionar_nivel/<int:mapa_id>/', views.seleccionar_nivel, name='seleccionar_nivel'),
    path('combatir_enemigo/<int:nivel_id>/', views.combatir_enemigo, name='combatir_enemigo'),


    #VENDEDORES
    path('vendedor_objetos/<str:tipo_vendedor>/', views.vendedor_objetos, name='vendedor_objetos'),
    path('comprar_objeto/<int:objeto_id>/', views.comprar_objeto, name='comprar_objeto'),
    path('consumir_objeto/<int:objeto_id>/', views.consumir_objeto, name='consumir_objeto'),
#    path('subastas/', views.listar_subastas, name='listar_subastas'),
#    path('crear_subasta/', views.crear_subasta, name='crear_subasta'),
#    path('comprar_subasta/<int:subasta_id>/', views.comprar_subasta, name='comprar_subasta'),
]
