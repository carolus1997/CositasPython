import geopandas as gpd
import os

# Define las rutas de las capas de entrada, la capa de provincias y el geodatabase de salida
capa_type = input("Introduce el tipo de capa que vas a usar (ej. rios, carreteras, etc): ")
capa_entrada_path = input("Introduce la ruta de la capa a recortar: ")
capa_provincias_path = input("Introduce la ruta de la capa de provincias: ")
gdb_output = input("Introduce la ruta de la carpeta de destino: ")
gdb_name = input("Introduce el nombre del gpkg de destino: ")
gdb_salida = os.path.join(gdb_output, gdb_name + ".gpkg")  # Usamos GeoPackage como formato de salida

# Carga las capas
capa_entrada = gpd.read_file(capa_entrada_path)
capa_provincias = gpd.read_file(capa_provincias_path)

# Obtiene una lista de las provincias en la capa de provincias
provincias = capa_provincias['NAME_2'].tolist()

# Sustituye las comillas simples en los nombres de las provincias por un carácter de escape de comilla simple
provincias_escaped = [provincia.replace("'", "_").replace("´", "") for provincia in provincias]

print(f"LISTA DE PRONVINCIAS: {provincias_escaped}")

# Recorre cada provincia
for provincia in provincias_escaped:
    # Selecciona la provincia actual
    provincia_geom = capa_provincias[capa_provincias['NAME_2'] == provincia].geometry.iloc[0]

    # Recorta la capa de entrada según los límites de la provincia actual
    capa_recortada = gpd.clip(capa_entrada, provincia_geom)

    # Define el nombre de la capa de salida
    nombre_capa_salida = f"{capa_type}_{provincia}"
    nombre_capa_salida = nombre_capa_salida.replace(" ", "_").replace("-", "_").replace("/", "")
    capa_salida_path = os.path.join(gdb_salida, nombre_capa_salida)

    # Guarda el resultado en la capa de salida
    capa_recortada.to_file(capa_salida_path, driver='GPKG')
    print(f'Se ha recortado la provincia de {provincia}')

print("PROCESO TERMINADO")