def calcular_salario_base(horas_trabajadas, tarifa_hora):
    if horas_trabajadas >= 40:
        return 40 * tarifa_hora
    return horas_trabajadas * tarifa_hora

def calcular_horas_extra_totales(horas_trabajadas):
    if horas_trabajadas > 40:
        horas_extra = horas_trabajadas - 40
        return horas_extra 
    return 0
    
def calcular_valor_horas_extra(horas_extra, tarifa_hora):
    return horas_extra * (tarifa_hora * 1.5)
    
def calcular_descuentos(salario_base, porcentaje_descuento):
    return salario_base * (porcentaje_descuento / 100)

def calcular_salario_neto(horas_trabajadas, tarifa_hora, porcentaje_descuento):
    salario_base = calcular_salario_base(horas_trabajadas, tarifa_hora)
    horas_extras = calcular_horas_extra_totales(horas_trabajadas)
    horas_extra_valor = calcular_valor_horas_extra(horas_extras, tarifa_hora)
    descuentos = calcular_descuentos(salario_base + horas_extra_valor, porcentaje_descuento)
    print(f"Salario base: ${salario_base:.2f}")
    print(f"Horas extra: {horas_extras} horas")
    print(f"Valor de horas extra: ${horas_extra_valor:.2f}")
    print(f"Total antes de descuentos: ${salario_base + horas_extra_valor:.2f}")
    print(f"Porcentaje de descuentos: {porcentaje_descuento}%")
    print(f"Valor de descuentos: ${descuentos:.2f}")
    print(f"Salario neto: ${salario_base + horas_extra_valor - descuentos:.2f}")
     



horas_trabajadas = float(input("Ingrese el número de horas trabajadas: "))
tarifa_hora = float(input("Ingrese la tarifa por hora: "))
porcentaje_descuento = float(input("Ingrese el porcentaje de descuento: "))
calcular_salario_neto(horas_trabajadas, tarifa_hora, porcentaje_descuento)
