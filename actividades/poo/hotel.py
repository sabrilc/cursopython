from abc import ABC, abstractmethod
from datetime import datetime
import re
import logging


logging.basicConfig(
    filename="hotel.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# --- Excepciones personalizadas ---

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


# --- Clase abstracta ---

class Habitacion(ABC):
    def __init__(self, numero, precio_por_noche, capacidad):
        self.numero = numero
        self.precio_por_noche = precio_por_noche
        self.capacidad = capacidad
        self.disponible = True

    @abstractmethod
    def calcular_precio(self, dias):
        pass

    @abstractmethod
    def mostrar_informacion(self):
        pass


# --- Clases concretas ---

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


# --- Clase Reserva ---

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
        logging.warning("Validacion fallo: nombre muy corto (%s)", nombre)
        raise DatosInvalidosError("El nombre debe tener al menos 3 caracteres")
    if not re.match(r"^[a-zA-Z\s]+$", nombre):
        logging.warning("Validacion fallo: nombre con caracteres invalidos (%s)", nombre)
        raise DatosInvalidosError("El nombre solo puede contener letras y espacios")
    return nombre.strip()


def validar_noches(noches):
    try:
        n = int(noches)
    except ValueError:
        logging.warning("Validacion fallo: noches no es numero entero (%s)", noches)
        raise DatosInvalidosError("El numero de noches debe ser un numero entero")
    if n <= 0:
        logging.warning("Validacion fallo: noches menor o igual a cero (%s)", noches)
        raise DatosInvalidosError("El numero de noches debe ser mayor a cero")
    return n


def validar_fechas(ingreso, salida):
    try:
        fecha_ing = datetime.strptime(ingreso, "%Y-%m-%d")
        fecha_sal = datetime.strptime(salida, "%Y-%m-%d")
    except ValueError:
        logging.warning("Validacion fallo: formato de fecha invalido (ingreso=%s, salida=%s)", ingreso, salida)
        raise FechaInvalidaError("Formato de fecha invalido. Use YYYY-MM-DD")
    if fecha_sal <= fecha_ing:
        logging.warning("Validacion fallo: salida (%s) anterior o igual a ingreso (%s)", salida, ingreso)
        raise FechaInvalidaError("La fecha de salida debe ser posterior a la fecha de ingreso")
    return fecha_ing, fecha_sal


# --- Sistema principal ---

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
            validar_nombre(nombre)

            print("\nHabitaciones disponibles:")
            disponibles = [h for h in self.habitaciones if h.disponible]
            if not disponibles:
                logging.warning("Intento de reserva sin habitaciones disponibles")
                print("No hay habitaciones disponibles.")
                return
            for h in disponibles:
                print(h.mostrar_informacion())

            num = input("\nNumero de habitacion: ")
            try:
                num = int(num)
            except ValueError:
                raise DatosInvalidosError("Debe ingresar un numero valido")

            habitacion = None
            for h in disponibles:
                if h.numero == num:
                    habitacion = h
                    break
            if not habitacion:
                raise HabitacionNoDisponibleError("Esa habitacion no esta disponible o no existe")

            fecha_ing = input("Fecha de ingreso (YYYY-MM-DD): ")
            fecha_sal = input("Fecha de salida (YYYY-MM-DD): ")
            fecha_ing, fecha_sal = validar_fechas(fecha_ing, fecha_sal)

            noches = (fecha_sal - fecha_ing).days
            validar_noches(noches)

            reserva = Reserva(nombre, habitacion, fecha_ing, fecha_sal)
            reserva.confirmar_reserva()
            self.reservas.append(reserva)
            logging.info("Reserva #%d creada - Huesped: %s, Habitacion: %s, Noches: %d, Total: $%.2f",
                         reserva.id, nombre, type(habitacion).__name__, noches, reserva.costo_total)
            print(f"\nReserva #{reserva.id} confirmada con exito!")
            print(f"Costo total: ${reserva.costo_total:.2f}")

        except (DatosInvalidosError, HabitacionNoDisponibleError, FechaInvalidaError) as e:
            logging.error("Error al crear reserva: %s", e)
            print(f"\nError: {e}")

    def cancelar_reserva(self):
        try:
            if not self.reservas:
                print("No hay reservas registradas.")
                return

            id_buscar = input("Numero de reserva a cancelar: ")
            try:
                id_buscar = int(id_buscar)
            except ValueError:
                raise DatosInvalidosError("Debe ingresar un numero valido")

            for r in self.reservas:
                if r.id == id_buscar:
                    if not r.activa:
                        print(f"La reserva #{id_buscar} ya esta cancelada.")
                        return
                    r.cancelar_reserva()
                    logging.info("Reserva #%d cancelada - Huesped: %s", r.id, r.huesped)
                    print(f"Reserva #{id_buscar} cancelada con exito.")
                    return

            raise ReservaNoEncontradaError(f"No se encontro la reserva #{id_buscar}")

        except (DatosInvalidosError, ReservaNoEncontradaError) as e:
            logging.error("Error al cancelar reserva: %s", e)
            print(f"\nError: {e}")

    def consultar_reservas(self):
        if not self.reservas:
            print("No hay reservas registradas.")
            return
        print("\n--- Reservas ---")
        for r in self.reservas:
            print(r.mostrar_reserva())
            print()

    def ejecutar(self):
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
                logging.critical("Sistema cerrado por el usuario")
                print("Gracias por preferir HOTEL PARADISE INN")
                break
            else:
                print("Opcion invalida. Intente de nuevo.")


if __name__ == "__main__":
    logging.info("=== INICIO DEL SISTEMA HOTEL PARADISE INN ===")
    hotel = Hotel()
    try:
        hotel.ejecutar()
    except Exception as e:
        logging.critical("Error critico no esperado: %s", e)
        raise
