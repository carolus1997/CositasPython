import arcpy
import os
from arcpy.sa import *

# Establecer el espacio de trabajo
ruta_de_datos=r"C:\Users\usuario\Documents\ArcGIS\Projects\Pythoneo\Data\BTN"
arcpy.env.workspace = r"C:\Users\usuario\Documents\ArcGIS\Projects\Pythoneo\Data\BTN\Colomera.gdb"

# Obtener una lista de todas las clases de entidades en el espacio de trabajo
feature_classes = arcpy.ListFeatureClasses()
print(feature_classes)

# Para datos vectoriales
for feature in feature_classes:
    if "NIV" in feature:
        # Obtener los nombres de los campos en la clase de entidades
        field_names = [f.name for f in arcpy.ListFields(feature)]
        for index, field in enumerate(field_names):
            print(f'[{index}] {field} ')
        indices_field = input("Elige el campo que representa la elevación (índices separados por comas): ")

        # Convertir los índices a enteros
        indices_campos_uso = [int(indice.strip()) for indice in indices_field.split(',')]

        for indice in indices_campos_uso:
            inContours = TopoContour([[feature, field_names[indice]]])
            DEM = TopoToRaster([inContours])
            DEM.save(os.path.join(ruta_de_datos, "{}.tif".format(feature)))
            arcpy.conversion.RasterToGeodatabase(DEM, arcpy.env.workspace)

    elif "DEM" in feature:
        pass
        # Realizar operaciones para DEM
        # TODO: Agregar código para procesar datos DEM

    # else:
    #     pass
    #     print(f"Se omitió {feature}.")
print("Procesamiento completado.")

            