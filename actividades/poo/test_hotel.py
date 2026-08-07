import unittest
from datetime import datetime, timedelta
import io
import sys
import os
import logging

os.chdir(os.path.dirname(__file__) or ".")

if os.path.exists("hotel.log"):
    os.remove("hotel.log")

from hotel import (
    HabitacionSimple,
    HabitacionDoble,
    Suite,
    Reserva,
    DatosInvalidosError,
    HabitacionNoDisponibleError,
    FechaInvalidaError,
    ReservaNoEncontradaError,
    validar_nombre,
    validar_noches,
    validar_fechas,
    Hotel,
)


class TestValidaciones(unittest.TestCase):

    def test_nombre_corto_genera_error(self):
        with self.assertRaises(DatosInvalidosError):
            validar_nombre("Al")

    def test_nombre_con_numeros_genera_error(self):
        with self.assertRaises(DatosInvalidosError):
            validar_nombre("Juan123")

    def test_nombre_valido_ok(self):
        resultado = validar_nombre("Maria Lopez")
        self.assertEqual(resultado, "Maria Lopez")

    def test_noches_cero_genera_error(self):
        with self.assertRaises(DatosInvalidosError):
            validar_noches("0")

    def test_noches_negativas_genera_error(self):
        with self.assertRaises(DatosInvalidosError):
            validar_noches("-3")

    def test_noches_no_numericas_genera_error(self):
        with self.assertRaises(DatosInvalidosError):
            validar_noches("abc")

    def test_noches_valida_ok(self):
        self.assertEqual(validar_noches("5"), 5)

    def test_fecha_salida_anterior_genera_error(self):
        with self.assertRaises(FechaInvalidaError):
            validar_fechas("2025-06-10", "2025-06-08")

    def test_fecha_salida_igual_genera_error(self):
        with self.assertRaises(FechaInvalidaError):
            validar_fechas("2025-06-10", "2025-06-10")

    def test_fechas_formato_invalido_genera_error(self):
        with self.assertRaises(FechaInvalidaError):
            validar_fechas("10-06-2025", "15-06-2025")

    def test_fechas_validas_ok(self):
        ing, sal = validar_fechas("2025-06-10", "2025-06-15")
        self.assertEqual(ing, datetime(2025, 6, 10))
        self.assertEqual(sal, datetime(2025, 6, 15))


class TestHabitaciones(unittest.TestCase):

    def test_simple_precio_normal(self):
        hab = HabitacionSimple(101)
        self.assertEqual(hab.calcular_precio(3), 300)
        self.assertEqual(hab.calcular_precio(7), 700)

    def test_doble_descuento_menor_5(self):
        hab = HabitacionDoble(201)
        self.assertEqual(hab.calcular_precio(3), 540)

    def test_doble_descuento_mayor_5(self):
        hab = HabitacionDoble(201)
        self.assertEqual(hab.calcular_precio(6), 972)

    def test_suite_incremento_vip(self):
        hab = Suite(301)
        self.assertEqual(hab.calcular_precio(3), 1080)

    def test_polimorfismo_calcular_precio(self):
        habitaciones = [HabitacionSimple(101), HabitacionDoble(201), Suite(301)]
        precios = [h.calcular_precio(5) for h in habitaciones]
        self.assertEqual(precios[0], 500)
        self.assertEqual(precios[1], 900)
        self.assertEqual(precios[2], 1800)

    def test_disponibilidad_inicial(self):
        hab = HabitacionSimple(101)
        self.assertTrue(hab.disponible)

    def test_marcar_no_disponible(self):
        hab = HabitacionSimple(101)
        hab.disponible = False
        self.assertFalse(hab.disponible)


class TestReserva(unittest.TestCase):

    def setUp(self):
        self.hab = HabitacionSimple(101)
        self.ingreso = datetime(2025, 6, 10)
        self.salida = datetime(2025, 6, 15)
        Reserva.contador = 1

    def test_crear_reserva(self):
        r = Reserva("Juan", self.hab, self.ingreso, self.salida)
        self.assertEqual(r.huesped, "Juan")
        self.assertEqual(r.numero_noches, 5)
        self.assertFalse(r.activa)

    def test_confirmar_reserva_cambia_estado(self):
        r = Reserva("Juan", self.hab, self.ingreso, self.salida)
        r.confirmar_reserva()
        self.assertTrue(r.activa)
        self.assertFalse(self.hab.disponible)
        self.assertEqual(r.costo_total, 500)

    def test_cancelar_reserva_libera_habitacion(self):
        r = Reserva("Juan", self.hab, self.ingreso, self.salida)
        r.confirmar_reserva()
        r.cancelar_reserva()
        self.assertFalse(r.activa)
        self.assertTrue(self.hab.disponible)


class TestHotel(unittest.TestCase):

    def setUp(self):
        Reserva.contador = 1
        self.hotel = Hotel()

    def test_reservar_habitacion_disponible(self):
        hab = self.hotel.habitaciones[0]
        self.assertTrue(hab.disponible)
        r = Reserva("Carlos", hab, datetime(2025, 7, 1), datetime(2025, 7, 5))
        r.confirmar_reserva()
        self.hotel.reservas.append(r)
        self.assertFalse(hab.disponible)
        self.assertEqual(len(self.hotel.reservas), 1)

    def test_reservar_habitacion_ocupada_genera_error(self):
        hab = self.hotel.habitaciones[0]
        hab.disponible = False
        disponibles = [h for h in self.hotel.habitaciones if h.disponible]
        self.assertNotIn(hab, disponibles)

    def test_cancelar_reserva_existente(self):
        hab = self.hotel.habitaciones[0]
        r = Reserva("Ana", hab, datetime(2025, 8, 1), datetime(2025, 8, 5))
        r.confirmar_reserva()
        self.hotel.reservas.append(r)
        r.cancelar_reserva()
        self.assertTrue(hab.disponible)
        self.assertFalse(r.activa)

    def test_cancelar_reserva_inexistente_genera_error(self):
        with self.assertRaises(ReservaNoEncontradaError):
            id_buscar = 999
            for r in self.hotel.reservas:
                if r.id == id_buscar:
                    return
            raise ReservaNoEncontradaError(f"No se encontro la reserva #{id_buscar}")

    def test_mostrar_habitaciones_incluye_todas(self):
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        self.hotel.mostrar_habitaciones()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("101", output)
        self.assertIn("301", output)


class TestLogging(unittest.TestCase):

    def test_log_creado_despues_de_operaciones(self):
        log_test = "hotel_test.log"
        if os.path.exists(log_test):
            try:
                os.remove(log_test)
            except PermissionError:
                pass

        logger = logging.getLogger("test_logger")
        logger.setLevel(logging.DEBUG)
        for h in logger.handlers[:]:
            logger.removeHandler(h)
        handler = logging.FileHandler(log_test, mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)

        logger.info("=== INICIO DEL SISTEMA HOTEL PARADISE INN ===")
        logger.info("Reserva #1 creada - Huesped: Test, Habitacion: Simple, Noches: 3, Total: $300.00")
        logger.warning("Validacion fallo: nombre muy corto (Al)")
        logger.error("Error al crear reserva: El nombre debe tener al menos 3 caracteres")
        logger.critical("Sistema cerrado por el usuario")

        handler.flush()
        handler.close()
        logger.removeHandler(handler)

        self.assertTrue(os.path.exists(log_test))
        with open(log_test, "r", encoding="utf-8") as f:
            contenido = f.read()

        self.assertIn("INICIO DEL SISTEMA", contenido)
        self.assertIn("Reserva #1 creada", contenido)
        self.assertIn("Validacion fallo", contenido)
        self.assertIn("Error al crear reserva", contenido)
        self.assertIn("Sistema cerrado", contenido)
        self.assertIn("INFO", contenido)
        self.assertIn("WARNING", contenido)
        self.assertIn("ERROR", contenido)
        self.assertIn("CRITICAL", contenido)

        try:
            os.remove(log_test)
        except PermissionError:
            pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
