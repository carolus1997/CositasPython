import arcpy
import os
from arcpy.sa import *
arcpy.env.overwriteOutput = True
# Establecer el espacio de trabajo
miGDB=r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\DatosIncendios\Incendios.gdb"
ruta_de_datos=r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\DatosIncendios"
arcpy.env.workspace = miGDB

# Obtener una lista de todas las clases de entidades en el espacio de trabajo
feature_classes = arcpy.ListFeatureClasses()
print(feature_classes)

# Para datos vectoriales
# Lista para guardar las capas para fusionar
layers_to_merge = []
for feature in feature_classes:
    if "NIV" in feature: #Aqui hay que añadir que tiene que poner cual es el elemento que más se repite en sus curvas de nivel
        # Agrega la capa a la lista de capas para fusionar
        layers_to_merge.append(feature)
        # Fusiona las capas
        output_layer = os.path.join(miGDB,"CurvasNivelTotal") # Cambia esto a la ruta de salida que desees
        arcpy.Merge_management(layers_to_merge, output_layer)
print("Curvas de nivel {} combiandas".format(layers_to_merge[-1]))
# Obtener los nombres de los campos en la clase de entidad fusionada
field_names = [f.name for f in arcpy.ListFields(output_layer)]
for index, field in enumerate(field_names):
    print(f'[{index}] {field} ')
indices_field = input("Elige el campo que representa la elevación (índices separados por comas): ")
# Convertir los índices a enteros
indices_campos_uso = [int(indice.strip()) for indice in indices_field.split(',')]
for indice in indices_campos_uso:
    inContours = TopoContour([[feature, field_names[indice]]])
    DEM = TopoToRaster([inContours])
    # DEM.save(os.path.join(ruta_de_datos, "{}.tif".format(feature)))
    arcpy.conversion.RasterToGeodatabase(DEM, arcpy.env.workspace)
    #
    # elif "DEM" in feature:
    #     pass
    #     # Realizar operaciones para DEM
    #     # TODO: Agregar código para procesar datos DEM

    # else:
    #     pass
    #     print(f"Se omitió {feature}.")
print("Procesamiento completado.")

            