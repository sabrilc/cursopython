from abc import ABC, abstractmethod

class Habitacion(ABC):
    def __init__(self, numero, precio, capacidad, disponible=True):
        self.numero = numero
        self.precio = precio
        self.capacidad = capacidad
        self.disponible = disponible

    @abstractmethod
    def calcular_precio(self, dias):
        """ Calcula el precio de una estadia"""
        pass

    @abstractmethod
    def mostrar_informacion(self):
        """ Muestra información de la habitación"""
        pass

    @staticmethod
    def obtener_habitaciones():
            with open("hotel.csv", "r", encoding="utf-8") as archivo:
                next(archivo) 
                for linea in archivo:
                    (numero, tipo, precio, capacidad,
                      disponible, cliente, fecha_ingreso, 
                    fecha_salida, dias_reservados,costo_total ) = linea.strip().split(",")
    
                    yield {
                        "numero": int(numero),
                        "tipo": tipo,
                        "precio": float(precio),
                        "capacidad": int(capacidad),
                        "disponible": disponible == "True",
                        "cliente":cliente,
                        "fecha_ingreso": fecha_ingreso,
                        "fecha_salida": fecha_salida,
                        "dias_reservados": dias_reservados,
                        "costo_total": costo_total
                    }

   


class HabitacionSimple(Habitacion):  
    def calcular_precio(self, dias):
        return self.precio * dias

    def mostrar_informacion(self):
        return super().mostrar_informacion()


class HabitacionDoble(Habitacion):

    def calcular_precio(self, dias):
       if dias > 5:
           return ( self.precio - (self.precio * 10)/100) * dias
       return self.precio * dias
    def mostrar_informacion(self):
            return super().mostrar_informacion()

    

class HabitacionSuite(Habitacion):

    def calcular_precio(self, dias):
        return (self.precio * 1.20) * dias

    def mostrar_informacion(self):
            return super().mostrar_informacion()
    

class Reserva:
    def __init__(
        self,
        huesped,
        habitacion,
        fecha_ingreso,
        fecha_salida,
        numero_noches,
        costo_total,
    ):
        self.huesped = huesped
        self.habitacion = habitacion
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.numero_noches = numero_noches
        self.costo_total = costo_total

    def confirmar_reserva(self):
        match self.habitacion['tipo']:
            case "simple":
                habitacion = HabitacionSimple(numero=self.habitacion["numero"],
                                              precio=self.habitacion["precio"],
                                              capacidad=self.habitacion["capacidad"],
                                              disponible=False)
            case "doble":
                habitacion = HabitacionDoble(numero=self.habitacion["numero"],
                                             precio=self.habitacion["precio"],
                                             capacidad=self.habitacion["capacidad"],
                                             disponible=False)

            case _:
                habitacion = HabitacionSuite(numero=self.habitacion["numero"],
                                             precio=self.habitacion["precio"],
                                             capacidad=self.habitacion["capacidad"],
                                             disponible=False)
        self.costo_total = habitacion.calcular_precio(self.numero_noches)
        habitaciones = []
        for h in Habitacion.obtener_habitaciones():            
            if h["numero"] == self.habitacion.get("numero"):               
                h["disponible"] = False
                h["huesped"] = self.huesped
                h["fecha_ingreso"] = self.fecha_ingreso
                h["fecha_salida"] = self.fecha_salida
                h["dias"] = self.numero_noches
                h["costo_total"] = self.costo_total

            habitaciones.append(h)
        with open("hotel.csv", "w", encoding="utf-8") as archivo:
            archivo.write("numero,tipo,precio,capacidad,disponible,cliente,fecha_ingreso,fecha_salida,dias_reservado,costo_total\n")
            for h in habitaciones:
                archivo.write(
                    f'{h["numero"]},{h["tipo"]},{h["precio"]},{h["capacidad"]},{h["disponible"]},{h.get("huesped","")},{h.get("fecha_ingreso","")},{h.get("fecha_salida","")},{h.get("dias","")},{h.get("costo_total","")}\n'
                )

    @staticmethod
    def cancelar_reserva(reserva):
        habitaciones = []
        for h in Habitacion.obtener_habitaciones():            
            if h["numero"] == reserva.get("numero"):               
                h["disponible"] = True
                h["huesped"] = ""
                h["fecha_ingreso"] = ""
                h["fecha_salida"] = ""
                h["dias"] = ""
                h["costo_total"] = ""

            habitaciones.append(h)
        with open("hotel.csv", "w", encoding="utf-8") as archivo:
            archivo.write("numero,tipo,precio,capacidad,disponible,cliente,fecha_ingreso, fecha_salida,dias_reservado,costo_total\n")
            for h in habitaciones:
                archivo.write(
                    f'{h["numero"]},{h["tipo"]},{h["precio"]},{h["capacidad"]},{h["disponible"]},{h.get("huesped","")},{h.get("fecha_ingreso","")},{h.get("fecha_salida","")},{h.get("dias","")},{h.get("costo_total","")}\n'
                )
        
    @staticmethod
    def mostrar_reservas():
        print("=========MOSTRANDO RESERVAS==========")
        print(
                    f"NUMERO    "
                    f"TIPO  "
                    f"CLIENTE   "
                    f"FECHA_INGRESO "
                    f"FECHA_SALIDA  "
                    f"DIAS_RESERVADOS   "
                    f"COSTO TOTAL   "                  
                )
        
        for habitacion in Habitacion.obtener_habitaciones():
            if habitacion.get("disponible") == False:
                print(
                    f"{habitacion['numero']}   "
                    f"{habitacion['tipo']}   "
                    f"{habitacion['cliente']}   "
                    f"{habitacion['fecha_ingreso']}   "
                    f"{habitacion['fecha_salida']}   "
                    f"{habitacion.get('dias_reservados',0)}"
                    f"{habitacion['costo_total']}   "                  
                )

class ErrorFormatoFecha(ValueError):
    def __str__(self):
        return "la fecha ingresado no esta con el formato(dd/mm/yyyy)"
    
            
