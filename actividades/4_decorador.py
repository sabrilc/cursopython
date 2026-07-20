from datetime import datetime


def mostrar_resultado(funcion):
    def wrapper(*args, **kwargs):
        # • Muestre fecha y hora
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{fecha_hora}]")
        
        # • Indique qué función se ejecutó
        print(f"Ejecutando la función: '{funcion.__name__}'")
        
        # Ejecutamos la función original guardando su resultado
        resultado = funcion(*args, **kwargs)
        
        # • Muestre el resultado
        print(f"Resultado obtenido: {resultado}")
             
        
        return resultado 
        
    return wrapper


@mostrar_resultado
def calcular_suma(a, b):
    return a + b

@mostrar_resultado
def saludar(nombre):
    return f"¡Hola, {nombre}!"



calcular_suma(5, 7)
saludar("Sergio")