import random

def aplicar_efecto(personaje, enemigo, efecto):
    resultado = {}

    if efecto == "critico":
        if random.random() < 0.1:  # Probabilidad de golpe crítico (10%)
            daño_critico = personaje.calcular_daño() * 2  # Golpe crítico duplicado
            resultado['daño'] = daño_critico
            resultado['mensaje'] = "¡Golpe crítico!"
        else:
            resultado['daño'] = personaje.calcular_daño()
    elif efecto == "invulnerabilidad":
        if random.random() < 0.01:  # Probabilidad de invulnerabilidad (1%)
            resultado['inmune'] = True
            resultado['mensaje'] = "¡Invulnerabilidad activada!"
        else:
            resultado['inmune'] = False
    return resultado