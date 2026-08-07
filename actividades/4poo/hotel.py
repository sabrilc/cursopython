import logging
import re
from datetime import datetime
from abc import ABC, abstractmethod


logging.basicConfig(
    filename="hotel.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


""" Exepciones """

class DatosInvalidosError(Exception):
    def __init__(self, mensaje="Datos invalidos ingresados"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class HabitacionNoDisponibleError(Exception):
    def __init__(self, mensaje="La habitacion no esta disponible"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class FechaInvalidaError(Exception):
    def __init__(self, mensaje="Fecha invalida"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ReservaNoEncontradaError(Exception):
    def __init__(self, mensaje="Reserva no encontrada"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class Habitacion(ABC):
    def __init__(self, numero, precio_por_noche, capacidad, disponible=True):
        self.numero = numero
        self.precio_por_noche = precio_por_noche
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

  
class HabitacionSimple(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, 100, 2)

    def calcular_precio(self, dias):
        return self.precio_por_noche * dias

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Simple #{self.numero} - ${self.precio_por_noche}/noche - Cap.{self.capacidad} - {estado}"


class HabitacionDoble(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, 180, 4)

    def calcular_precio(self, dias):
        total = self.precio_por_noche * dias
        if dias > 5:
            total *= 0.9
        return total

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Doble #{self.numero} - ${self.precio_por_noche}/noche - Cap.{self.capacidad} - {estado} (10% desc >5 noches)"


class Suite(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, 300, 2)

    def calcular_precio(self, dias):
        total = self.precio_por_noche * dias
        total *= 1.2
        return total

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Suite #{self.numero} - ${self.precio_por_noche}/noche - Cap.{self.capacidad} - {estado} (+20% VIP)"

class Reserva:
    contador = 1

    def __init__(self, huesped, habitacion, fecha_ingreso, fecha_salida):
        self.id = Reserva.contador
        Reserva.contador += 1
        self.huesped = huesped
        self.habitacion = habitacion
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.numero_noches = (fecha_salida - fecha_ingreso).days
        self.costo_total = 0
        self.activa = False

    def confirmar_reserva(self):
        self.activa = True
        self.habitacion.disponible = False
        self.costo_total = self.habitacion.calcular_precio(self.numero_noches)

    def cancelar_reserva(self):
        self.activa = False
        self.habitacion.disponible = True

    def mostrar_reserva(self):
        estado = "Activa" if self.activa else "Cancelada"
        return (
            f"Reserva #{self.id} - {estado}\n"
            f"  Huesped: {self.huesped}\n"
            f"  Habitacion: {self.habitacion.mostrar_informacion()}\n"
            f"  Ingreso: {self.fecha_ingreso.date()}\n"
            f"  Salida: {self.fecha_salida.date()}\n"
            f"  Noches: {self.numero_noches}\n"
            f"  Costo total: ${self.costo_total:.2f}"
        )

           
# --- Validaciones ---

def validar_nombre(nombre):
    if len(nombre) < 3:
        raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres")
    if not re.match(r"^[a-zA-Z\s]+$", nombre):
        raise DatosInvalidosError("El nombre solo puede contener letras y espacios")
    return nombre.strip()


def validar_noches(noches):
    try:
        n = int(noches)
    except ValueError:
        raise DatosInvalidosError("El numero de noches debe ser un numero entero")
    if n <= 0:
        raise DatosInvalidosError("El numero de noches debe ser mayor a cero")
    return n


def validar_fechas(ingreso, salida):
    try:
        fecha_ing = datetime.strptime(ingreso, "%Y-%m-%d")
        fecha_sal = datetime.strptime(salida, "%Y-%m-%d")
    except ValueError:
        raise FechaInvalidaError("Formato de fecha invalido. Use YYYY-MM-DD")
    if fecha_sal <= fecha_ing:
        raise FechaInvalidaError("La fecha de salida debe ser posterior a la fecha de ingreso")
    return fecha_ing, fecha_sal




def crear_reserva(hotel, nombre, num_habitacion, fecha_ing_str, fecha_sal_str):
    try:
        nombre = validar_nombre(nombre)

        disponibles = [h for h in hotel.habitaciones if h.disponible]
        if not disponibles:
            raise HabitacionNoDisponibleError("No hay habitaciones disponibles")

        try:
            num = int(num_habitacion)
        except ValueError:
            raise DatosInvalidosError("Debe ingresar un numero valido")

        habitacion = None
        for h in disponibles:
            if h.numero == num:
                habitacion = h
                break
        if not habitacion:
            raise HabitacionNoDisponibleError("Esa habitacion no esta disponible o no existe")

        fecha_ing, fecha_sal = validar_fechas(fecha_ing_str, fecha_sal_str)
        noches = (fecha_sal - fecha_ing).days
        validar_noches(noches)

        reserva = Reserva(nombre, habitacion, fecha_ing, fecha_sal)
        reserva.confirmar_reserva()
        hotel.reservas.append(reserva)
        logger.info(f"Reserva #{reserva.id} creada - Huesped: {nombre}, Habitacion: {habitacion.numero}")
        return reserva

    except (DatosInvalidosError, HabitacionNoDisponibleError, FechaInvalidaError) as e:
        logger.error(f"Error de validacion al crear reserva: {e}")
        raise


def cancelar_reserva_por_id(hotel, id_reserva):
    try:
        try:
            id_buscar = int(id_reserva)
        except ValueError:
            raise DatosInvalidosError("Debe ingresar un numero valido")

        for r in hotel.reservas:
            if r.id == id_buscar:
                if not r.activa:
                    logger.warning(f"Intento de cancelar reserva #{id_buscar} que ya estaba cancelada")
                    return f"La reserva #{id_buscar} ya esta cancelada."
                r.cancelar_reserva()
                logger.warning(f"Reserva #{id_buscar} cancelada - Huesped: {r.huesped}")
                return f"Reserva #{id_buscar} cancelada con exito."

        raise ReservaNoEncontradaError(f"No se encontro la reserva #{id_buscar}")

    except (DatosInvalidosError, ReservaNoEncontradaError) as e:
        logger.error(f"Error al cancelar reserva: {e}")
        raise


class Hotel:
    def __init__(self):
        self.habitaciones = [
            HabitacionSimple(101),
            HabitacionSimple(102),
            HabitacionDoble(201),
            HabitacionDoble(202),
            Suite(301),
            Suite(302),
        ]
        self.reservas = []

    def mostrar_habitaciones(self):
        print("\n--- Habitaciones ---")
        for hab in self.habitaciones:
            print(hab.mostrar_informacion())

    def realizar_reserva(self):
        try:
            nombre = input("Nombre del huesped: ")
            print("\nHabitaciones disponibles:")
            for h in [h for h in self.habitaciones if h.disponible]:
                print(h.mostrar_informacion())
            num = input("\nNumero de habitacion: ")
            fecha_ing = input("Fecha de ingreso (YYYY-MM-DD): ")
            fecha_sal = input("Fecha de salida (YYYY-MM-DD): ")
            reserva = crear_reserva(self, nombre, num, fecha_ing, fecha_sal)
            print(f"\nReserva #{reserva.id} confirmada con exito!")
            print(f"Costo total: ${reserva.costo_total:.2f}")
        except (DatosInvalidosError, HabitacionNoDisponibleError, FechaInvalidaError) as e:
            print(f"\nError: {e}")
        except Exception as e:
            logger.critical(f"Excepcion no esperada en realizar_reserva: {e}")
            print(f"\nError inesperado: {e}")

    def cancelar_reserva(self):
        try:
            if not self.reservas:
                print("No hay reservas registradas.")
                return
            id_buscar = input("Numero de reserva a cancelar: ")
            mensaje = cancelar_reserva_por_id(self, id_buscar)
            print(mensaje)
        except (DatosInvalidosError, ReservaNoEncontradaError) as e:
            print(f"\nError: {e}")
        except Exception as e:
            logger.critical(f"Excepcion no esperada en cancelar_reserva: {e}")
            print(f"\nError inesperado: {e}")

    def consultar_reservas(self):
        if not self.reservas:
            print("No hay reservas registradas.")
            return
        print("\n--- Reservas ---")
        for r in self.reservas:
            print(r.mostrar_reserva())
            print()

    def ejecutar(self):
        logger.info("Sistema iniciado")
        while True:
            print("\n===== HOTEL PARADISE INN =====")
            print("1. Mostrar habitaciones")
            print("2. Realizar reserva")
            print("3. Cancelar reserva")
            print("4. Consultar reservas")
            print("5. Salir")
            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                self.mostrar_habitaciones()
            elif opcion == "2":
                self.realizar_reserva()
            elif opcion == "3":
                self.cancelar_reserva()
            elif opcion == "4":
                self.consultar_reservas()
            elif opcion == "5":
                logger.info("Sistema cerrado por el usuario")
                print("Gracias por preferir HOTEL PARADISE INN")
                break
            else:
                logger.warning(f"Opcion invalida ingresada: {opcion}")
                print("Opcion invalida. Intente de nuevo.")


if __name__ == "__main__":
    logger.info("Programa iniciado")
    try:
        hotel = Hotel()
        hotel.ejecutar()
    except Exception as e:
        logger.critical(f"Error critico en la ejecucion del programa: {e}")
    finally:
        logger.info("Programa finalizado")

