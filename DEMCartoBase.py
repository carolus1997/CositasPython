import arcpy
import os
from arcpy.sa import *
arcpy.env.overwriteOutput = True

# ESPACIO DE TRABAJO
miGDB = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\CurvasNivel\CurvasNivelPruebaDEM.gdb"
ruta_de_datos = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\CurvasNivel"
arcpy.env.workspace = miGDB

# OBTENER Y MOSTRAR CLASES DE ENTIDAD
feature_classes = arcpy.ListFeatureClasses()
print("Feature classes: ", feature_classes)

# CREAR RASTERS
for capa in feature_classes:
    if "NIV" in capa or "contour" in capa:
        field_names = [f.name for f in arcpy.ListFields(capa)]
        for index, field in enumerate(field_names):
            print(f'[{index}] {field}')
        indices_field = input("Elige el campo que representa la elevación (índices separados por comas): ")
        indices_campos_uso = [int(indice.strip()) for indice in indices_field.split(',')]
        for indice in indices_campos_uso:
            # Eliminar el raster antiguo si existe
            arcpy.Delete_management("DEM_" + field_names[indice], "")
            # Crear el raster nuevo
            arcpy.CheckOutExtension("Spatial")
            inContours = TopoContour([[capa, field_names[indice]]])
            DEM = TopoToRaster([inContours])
            arcpy.conversion.RasterToGeodatabase(DEM, arcpy.env.workspace, "DEM_" + field_names[indice])
            print("DEM Created")

# OBTENER Y MOSTRAR RASTERS
rasters = arcpy.ListRasters("*", "All")
print("Rasters: ", rasters)

# CREAR HILLSHADES Y SLOPES
for raster in rasters:
    if "DEM" in raster:
        # Eliminar el hillshade antiguo si existe
        arcpy.Delete_management("Hillshade_" + raster, "")
        # Crear el hillshade nuevo
        arcpy.CheckOutExtension("Spatial")
        outHillshade = Hillshade(raster)
        arcpy.conversion.RasterToGeodatabase(outHillshade, arcpy.env.workspace, "Hillshade_" + raster)
        print("Hillshade Generado")
        # Eliminar el slope antiguo si existe
        arcpy.Delete_management("Slope_" + raster, "")
        # Crear el slope nuevo
        outSlope = Slope(raster, "DEGREE")
        arcpy.conversion.RasterToGeodatabase(outSlope, arcpy.env.workspace, "Slope_" + raster)
        print("Slope Generado")

print("Procesamiento completado.")
