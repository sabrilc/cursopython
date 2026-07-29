import logging
from datetime import datetime

from clases import Habitacion, Reserva, HabitacionNoDisponibleError, DatosInvalidosError ,ReservaNoEncontradaError, FechaInvalidaError

class HotelService:
    def iniciar_atencion(self):
        print("===========HOTEL PARADISE INN ===========")
        print("1. Mostrar habitaciones")
        print("2. Realizar reserva")
        print("3. Cancelar reserva")
        print("4. Consultar reservas")
        print("5. Salir")
        opcion = self.leer_opcion()

        match opcion:
            case 1:
                self.pantallan_mostrar_habitaciones()

            case 2:
                self.pantalla_realizar_reserva()

            case 3:
                self.pantalla_cancelar_reserva()

            case 4:
                self.pantalla_consultar_reservas()

            case 5:
                logging.info("Sistema apagado")
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

    def pantallan_mostrar_habitaciones(self):
        print("=========MOSTRANDO HABITACIONES==========")
        for habitacion in Habitacion.obtener_habitaciones():
            print(
                f"{habitacion['numero']}   "
                f"{habitacion['tipo']}   "
                f"{habitacion['precio']}   "
                f"{habitacion['capacidad']}   "
                f"{'DISPONIBLE' if habitacion['disponible'] else 'OCUPADA'}"
            )

    def pantalla_consultar_reservas(self):
        Reserva.mostrar_reservas()

   

    def pantalla_realizar_reserva(self):
        self.pantallan_mostrar_habitaciones()
        habitacion = self.obtener_habitacion_disponible()
        huesped = self.leer_huesped()
        numero_noches = self.leer_numero_noches()
        fecha_ingreso, fecha_salida= self.leer_fechas_reserva()        

        reserva = Reserva(huesped=huesped, 
                          habitacion=habitacion, 
                          numero_noches=numero_noches,
                          fecha_ingreso=fecha_ingreso,
                          fecha_salida=fecha_salida,
                          costo_total=0)

        reserva.confirmar_reserva()     
        logging.info(f"Se creo la reserva en la habitacion{habitacion['numero']} para el cliente {huesped} dias totales {numero_noches} fecha de ingreso {  fecha_ingreso}")   


    def pantalla_cancelar_reserva(self):
        Reserva.mostrar_reservas()
        reserva = self.obtener_reserva()       
        Reserva.cancelar_reserva(reserva=reserva)
        logging.info(f"Se cancelo la reserva en la habitacion numero {reserva.get("numero")}")
      

    def obtener_habitacion_disponible(self):
        while True:
            try:
                numero = int(input("Ingrese el numero de habitacion: "))
                habitacion = self.buscar_habitacion(numero)
                if habitacion is None:
                    print(f"La habitacion numero('{numero}') no existe")
                    continue
                if habitacion['disponible']== False:
                    raise HabitacionNoDisponibleError                        
                return habitacion

            except Exception as error:
                logging.warn(error)
                print(error)

    def obtener_reserva(self):
        while True:
            try:
                numero = int(input("Ingrese el numero de habitacion: "))
                habitacion = self.buscar_habitacion(numero)
                if habitacion is None:
                    print(f"La habitacion numero('{numero}') no existe")
                    continue
                if habitacion['disponible']== True:
                        raise ReservaNoEncontradaError                        
                return habitacion

            except Exception as error:
                logging.warn(error)
                print(error)

    

    def buscar_habitacion(self, numero):
        return next(
           ( habitacion for habitacion in Habitacion.obtener_habitaciones()
            if habitacion["numero"] == numero ),
            None,
        )

    

    def leer_huesped(self):
        while True:
            try:
                huesped = str( input("Ingrese le nombre del huesped: "))
                if len(huesped.strip()) < 3:
                    raise DatosInvalidosError
                return huesped
            except Exception as error:
                logging.critical(error)
                print("Debe ingresar un nombre de huesped valido")

    def leer_numero_noches(self):
        while True:
            try:
                noches = int( input("ingrese el numero de noches: "))
                if noches < 0:
                    print("El numero de noches debe ser mayor a cero")
                    continue
                return noches

            except ValueError as error:
                logging.warn(error)
                print("Debe ingresar un numero entero")

    def leer_fechas_reserva(self):
        while True:
            try:
                fecha_ingreso= input("Fecha ingreso(dd/mm/yyyy): ")
                fecha_salida= input("Fecha salida(dd/mm/yyyy): ")

                fecha_ingreso= datetime.strptime(fecha_ingreso,"%d/%m/%Y")
                fecha_salida= datetime.strptime(fecha_salida, "%d/%m/%Y")

                if( fecha_salida < fecha_ingreso):
                    print("fecha salida no puede ser aterior a la fecha de ingreso")
                    continue

                return fecha_ingreso, fecha_salida

            except FechaInvalidaError as error:
                logging.error(error)
                print(error)

            

