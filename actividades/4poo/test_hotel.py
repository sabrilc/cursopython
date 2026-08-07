import os
from hotel import (
    Hotel,
    Reserva,
    HabitacionSimple,
    HabitacionDoble,
    Suite,
    validar_nombre,
    crear_reserva,
    cancelar_reserva_por_id,
    DatosInvalidosError,
    HabitacionNoDisponibleError,
    FechaInvalidaError,
    ReservaNoEncontradaError,
)


# ======== Caso 1: Registrar huesped con nombre de 2 letras ========

def test_nombre_corto_lanza_error():
    try:
        validar_nombre("Al")
        assert False, "Debio lanzar DatosInvalidosError"
    except DatosInvalidosError:
        pass


def test_nombre_valido_ok():
    assert validar_nombre("  Juan Perez  ") == "Juan Perez"


def test_nombre_con_numeros_lanza_error():
    try:
        validar_nombre("Juan123")
        assert False, "Debio lanzar DatosInvalidosError"
    except DatosInvalidosError:
        pass


# ======== Caso 2: Reservar habitacion disponible ========

def test_reservar_habitacion_disponible():
    Reserva.contador = 1
    hotel = Hotel()
    reserva = crear_reserva(hotel, "Juan Perez", "101", "2026-08-01", "2026-08-05")
    assert reserva is not None
    assert reserva.id == 1
    assert reserva.huesped == "Juan Perez"
    assert reserva.habitacion.numero == 101
    assert reserva.activa is True
    assert reserva.habitacion.disponible is False


# ======== Caso 3: Reservar habitacion ocupada ========

def test_reservar_habitacion_ocupada():
    Reserva.contador = 1
    hotel = Hotel()
    crear_reserva(hotel, "Juan Perez", "101", "2026-08-01", "2026-08-05")
    try:
        crear_reserva(hotel, "Maria Lopez", "101", "2026-08-10", "2026-08-15")
        assert False, "Debio lanzar HabitacionNoDisponibleError"
    except HabitacionNoDisponibleError:
        pass


def test_reservar_habitacion_inexistente():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Juan Perez", "999", "2026-08-01", "2026-08-05")
        assert False, "Debio lanzar HabitacionNoDisponibleError"
    except HabitacionNoDisponibleError:
        pass


def test_reservar_numero_habitacion_invalido():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Juan Perez", "abc", "2026-08-01", "2026-08-05")
        assert False, "Debio lanzar DatosInvalidosError"
    except DatosInvalidosError:
        pass


# ======== Caso 4: Reservar con fechas invalidas ========

def test_salida_anterior_a_ingreso():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Juan Perez", "101", "2026-08-10", "2026-08-05")
        assert False, "Debio lanzar FechaInvalidaError"
    except FechaInvalidaError:
        pass


def test_salida_igual_a_ingreso():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Juan Perez", "101", "2026-08-05", "2026-08-05")
        assert False, "Debio lanzar FechaInvalidaError"
    except FechaInvalidaError:
        pass


def test_formato_fecha_invalido():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Juan Perez", "101", "01-08-2026", "05-08-2026")
        assert False, "Debio lanzar FechaInvalidaError"
    except FechaInvalidaError:
        pass


# ======== Caso 5: Cancelar reserva existente ========

def test_cancelar_reserva_existente():
    Reserva.contador = 1
    hotel = Hotel()
    reserva = crear_reserva(hotel, "Juan Perez", "101", "2026-08-01", "2026-08-05")
    mensaje = cancelar_reserva_por_id(hotel, "1")
    assert "cancelada con exito" in mensaje
    assert reserva.activa is False
    assert reserva.habitacion.disponible is True


# ======== Caso 6: Cancelar reserva inexistente ========

def test_cancelar_reserva_inexistente():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        cancelar_reserva_por_id(hotel, "999")
        assert False, "Debio lanzar ReservaNoEncontradaError"
    except ReservaNoEncontradaError:
        pass


def test_cancelar_reserva_id_invalido():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        cancelar_reserva_por_id(hotel, "abc")
        assert False, "Debio lanzar DatosInvalidosError"
    except DatosInvalidosError:
        pass


# ======== Caso 7: Calcular precio de cada tipo de habitacion (polimorfismo) ========

def test_precio_habitacion_simple():
    hab = HabitacionSimple(101)
    assert hab.calcular_precio(3) == 300
    assert hab.calcular_precio(7) == 700


def test_precio_habitacion_doble_sin_descuento():
    hab = HabitacionDoble(201)
    assert hab.calcular_precio(5) == 900


def test_precio_habitacion_doble_con_descuento():
    hab = HabitacionDoble(201)
    assert hab.calcular_precio(6) == 180 * 6 * 0.9


def test_precio_suite():
    hab = Suite(301)
    assert hab.calcular_precio(4) == 300 * 4 * 1.2


def test_polimorfismo_precios():
    simple = HabitacionSimple(101).calcular_precio(3)
    doble = HabitacionDoble(201).calcular_precio(3)
    suite = Suite(301).calcular_precio(3)
    assert simple == 300
    assert doble == 540
    assert suite == 1080


# ======== Caso 8: Revisar archivo hotel.log ========

def test_log_contiene_eventos():
    if os.path.exists("hotel.log"):
        with open("hotel.log", "w", encoding="utf-8"):
            pass
    Reserva.contador = 1
    hotel = Hotel()
    crear_reserva(hotel, "Juan Perez", "101", "2026-08-01", "2026-08-05")
    cancelar_reserva_por_id(hotel, "1")
    with open("hotel.log", encoding="utf-8") as f:
        contenido = f.read()
    assert "INFO" in contenido
    assert "Reserva #1" in contenido
    assert "WARNING" in contenido


def test_log_contiene_errores():
    Reserva.contador = 1
    hotel = Hotel()
    try:
        crear_reserva(hotel, "Al", "101", "2026-08-01", "2026-08-05")
    except DatosInvalidosError:
        pass
    with open("hotel.log", encoding="utf-8") as f:
        contenido = f.read()
    assert "ERROR" in contenido
    assert "Error de validacion" in contenido


# ======== Ejecutor ========

def ejecutar_tests():
    tests = [
        test_nombre_corto_lanza_error,
        test_nombre_valido_ok,
        test_nombre_con_numeros_lanza_error,
        test_reservar_habitacion_disponible,
        test_reservar_habitacion_ocupada,
        test_reservar_habitacion_inexistente,
        test_reservar_numero_habitacion_invalido,
        test_salida_anterior_a_ingreso,
        test_salida_igual_a_ingreso,
        test_formato_fecha_invalido,
        test_cancelar_reserva_existente,
        test_cancelar_reserva_inexistente,
        test_cancelar_reserva_id_invalido,
        test_precio_habitacion_simple,
        test_precio_habitacion_doble_sin_descuento,
        test_precio_habitacion_doble_con_descuento,
        test_precio_suite,
        test_polimorfismo_precios,
        test_log_contiene_eventos,
        test_log_contiene_errores,
    ]

    resultados = []
    for test in tests:
        try:
            test()
            resultados.append((test.__name__, "PASO"))
        except AssertionError as e:
            resultados.append((test.__name__, f"FALLO: {e}"))
        except Exception as e:
            resultados.append((test.__name__, f"ERROR: {e}"))

    print("--- Resultados ---")
    for nombre, estado in resultados:
        print(f"  {nombre}: {estado}")
    total = len(resultados)
    pasaron = sum(1 for _, e in resultados if e == "PASO")
    print(f"\nTotal: {total} | Pasaron: {pasaron} | Fallaron: {total - pasaron}")


if __name__ == "__main__":
    ejecutar_tests()
