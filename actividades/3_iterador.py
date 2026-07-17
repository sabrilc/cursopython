#Clase que implemnta metodos para realizar una tabla de multiplicación, mediante iteradores
class TablaMultiplicar:
    """Método constructor de la clase en el cual obligariamente recibe el numero al que se le va
    a construir la tabla y opcionamente tambiens epude definer el limite de los numeros multiplicadores"""
    def __init__(self,numero, limite=12):
        self.numero = numero
        self.limite = limite
        self.multiplicador=0
    """Método que devuelve el iterador del objeto para permitir recorrer sus elementos"""   
    def __iter__(self):
        return self
    
    """Método que devuelve el siguiente elemento de la tabla validado que no supere el limite del multiplicador,
    realiza el incremento del multiplicador,
    luego procede a realizar la multiplicación del numero * el multiplicador correspondiente""" 
    def __next__(self):
        if self.multiplicador < self.limite:
            self.multiplicador += 1
            return self.multiplicador * self.numero
        
        raise StopIteration
    
    
            
#Creo un objeto iterador llamado tabla5 en base a mi clase TablaMultiplicar
tabla = TablaMultiplicar(2,22)

#Itero los resultados de la tabla de multiplicar
for resultado in tabla:
    print(resultado)
    
#Intento iterar a fin de verificar si se lanza la excepcion cuando no ya se ha superado el limite de multiplicadores   
print(next(tabla))

    