import logging


class Hotel:
    def iniciar_atencion(self):
        print("===========HOTEL PARADISE INN ===========")
        print("1. Mostrar habitaciones")
        print("2. Realizar reserva")
        print("3. Cancelar reserva")
        print("4. Consultar reservas")
        print("5. Salir")
        print("Selecciones una opcion:")
        opcion = self.leer_opcion()

        match opcion:
            case 1:
                self.mostrar_habitaciones()

            case 2:
                self.realizar_reserva()

            case 3:
                self.cancelar_reserva()

            case 4:
                self.consultar_reserva

            case 5:
                exit()

    def leer_opcion(self):
        while True:
            try:
                opcion = int(input("Seleccione una opcion: "))
                if opcion < 1 or opcion > 5:
                    print(f"La opcion seleccionada '{opcion}' esta fuera de contexto")
                    continue
                return opcion

            except ValueError as error:
                logging.warn(error)

                print("Debe ingresar un número")

    def mostrar_habitaciones(self):
        print("=========MOSTRANDO HABITACIONES==========")
        for habitacion in self.cargar_habitaciones():
            print(
                f"{habitacion['numero']}   "
                f"{habitacion['tipo']}   "
                f"{habitacion['precio']}   "
                f"{habitacion['capacidad']}   "
                f"{'DISPONIBLE' if habitacion['disponible'] else 'OCUPADA'}"
            )
    def cargar_habitaciones(self):
        with open("hotel.csv", "r", encoding="utf-8") as archivo:
            next(archivo) 
            for linea in archivo:
                numero, tipo, precio, capacidad, disponible = linea.strip().split(",")

                yield {
                    "numero": int(numero),
                    "tipo": tipo,
                    "precio": float(precio),
                    "capacidad": int(capacidad),
                    "disponible": disponible == "True",
                }
