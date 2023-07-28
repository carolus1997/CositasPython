import arcpy
import os
from arcpy.sa import *
arcpy.env.overwriteOutput = True
# Establecer el espacio de trabajo
miGDB=r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\DatosIncendios\CartoBasePrueba.gdb"
ruta_de_datos=r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\DatosIncendios"
arcpy.env.workspace = miGDB

# Obtener una lista de todas las clases de entidades en el espacio de trabajo
feature_classes = arcpy.ListFeatureClasses()
print(feature_classes)

# Para datos vectoriales
# Lista para guardar las capas para fusionar
layers_to_merge = []
for feature in feature_classes:
    if "NIV" in feature or "contour" in feature: #Aqui hay que añadir que tiene que poner cual es el elemento que más se repite en sus curvas de nivel
        # Agrega la capa a la lista de capas para fusionar
        layers_to_merge.append(feature)

# Fusiona las capas después de que todas las capas hayan sido agregadas a la lista
if len(layers_to_merge)>1:
    output_layer = os.path.join(miGDB,"CurvasNivelTotal") # Cambia esto a la ruta de salida que desees
    arcpy.Merge_management(layers_to_merge, output_layer)
    print("Curvas de nivel combinadas")
else:
    output_layer = os.path.join(miGDB, "CurvasNivelTotal")
    print("Solo hay una capa")

# Obtener los nombres de los campos en la clase de entidad fusionada
feature_classes = arcpy.ListFeatureClasses()
for capa in feature_classes:
    if "CurvasNivelTotal" in capa:
        field_names = [f.name for f in arcpy.ListFields(capa)]
        for index, field in enumerate(field_names):
            print(f'[{index}] {field} ')
        indices_field = input("Elige el campo que representa la elevación (índices separados por comas): ")
        # Convertir los índices a enteros
        indices_campos_uso = [int(indice.strip()) for indice in indices_field.split(',')]
for indice in indices_campos_uso:
    inContours = TopoContour([[feature, field_names[indice]]])
    DEM = TopoToRaster([inContours])
    output_dem_name = f"{feature}_DEM"
    output_dem_path = os.path.join(miGDB, output_dem_name)
    DEM.save(os.path.join(ruta_de_datos,"{}.tif".format(output_dem_name)))

# Una vez creado el DEM, creamos el Hillshade y Slope
# Hillshade
arcpy.env.workspace = ruta_de_datos
rasters = arcpy.ListRasters("*", "All")
for raster in rasters:
    print(raster)
    outHillshade = Hillshade(raster)
    outHillshade.save(os.path.join(ruta_de_datos, "Hillshade.tif"))
    print("Hillshade Generado")

    # Slope
    outSlope = Slope(raster, "DEGREE")
    outSlope.save(os.path.join(ruta_de_datos, "Slope.tif"))
    print("Slope Generado")
rasters = arcpy.ListRasters("*", "GRID")
rasters_string = ";".join(rasters)
arcpy.conversion.RasterToGeodatabase(rasters_string, "CartoBasePrueba.gdb")
print("Procesamiento completado.")


            