def calcular_salario_base(horas_trabajadas, tarifa_hora):
    return horas_trabajadas * tarifa_hora

def calcular_horas_extra(horas_trabajadas, tarifa_hora):
    if horas_trabajadas > 40:
        horas_extra = horas_trabajadas - 40
        return horas_extra * (tarifa_hora * 1.5)
    else:
        return 0
    
def calcular_descuentos(salario_base, porcentaje_descuento):
    return salario_base * (porcentaje_descuento / 100)

def calcular_salario_neto(horas_trabajadas, tarifa_hora, porcentaje_descuento):
    salario_base = calcular_salario_base(horas_trabajadas, tarifa_hora)
    horas_extra = calcular_horas_extra(horas_trabajadas, tarifa_hora)
    descuentos = calcular_descuentos(salario_base + horas_extra, porcentaje_descuento)
    
    salario_neto = salario_base + horas_extra - descuentos
    return salario_neto


horas_trabajadas = float(input("Ingrese el número de horas trabajadas: "))
tarifa_hora = float(input("Ingrese la tarifa por hora: "))
porcentaje_descuento = float(input("Ingrese el porcentaje de descuento: "))

salario_neto = calcular_salario_neto(horas_trabajadas, tarifa_hora, porcentaje_descuento)
print(f"El salario neto es: ${salario_neto:.2f}")