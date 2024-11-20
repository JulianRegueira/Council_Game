from django.contrib.auth.models import User

from Council_Game.Characters.models import Heroe, Inventario, Objeto

# Obtener el usuario y su héroe
user = User.objects.get(username='Admin_HeroeV3')
heroe = Heroe.objects.get(user=user)

# Obtener el inventario del héroe
inventario = Inventario.objects.get(heroe=heroe)

# Agregar un item al inventario
item = Objeto.objects.first()  # Asegúrate de tener un objeto creado
inventario.items.add(item)
inventario.save()
