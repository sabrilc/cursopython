import pandas as pd


df = pd.read_csv("ventas_tienda.csv")


print("===== DATOS DEL ARCHIVO =====")
print(df.head())

# 1. Productos con ventas mayores a 500
print("\n1. Productos con ventas mayores a 500")
ventas_mayores = df[df["ventas"] > 500]
print(ventas_mayores[["producto", "ventas"]])

# 2. Ventas de Quito
print("\n2. Ventas de Quito")
ventas_quito = df[df["ciudad"] == "Quito"]
print(ventas_quito)

# 3. Productos ordenados por precio
print("\n3. Productos ordenados por precio")
ordenados = df.sort_values(by="precio_unitario")
print(ordenados[["producto", "precio_unitario"]])

# 4. Cinco productos más vendidos
print("\n4. Cinco productos más vendidos")
top5 = df.sort_values(by="ventas", ascending=False).head(5)
print(top5[["producto", "ventas"]])

# 5. Ventas superiores al promedio
print("\n5. Ventas superiores al promedio")

promedio = df["ventas"].mean()
print("Promedio de ventas:", promedio)

superiores = df[df["ventas"] > promedio]
print(superiores[["producto", "ventas"]])