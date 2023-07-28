import arcpy
import os
from arcpy.sa import *
# Esta función permite, con una ruta y un nombre de una gdb, poder gestionar de primeras la creación y población de una gdb si la necesitamos


def gestionar_gdb(ruta_datos, nombre_gdb):
    carpeta_datos_shp = ruta_datos
    mi_gdb = os.path.join(carpeta_datos_shp, "{}.gdb".format(nombre_gdb))
    print(mi_gdb)

    if arcpy.Exists(mi_gdb):
        print("Tu gdb ya existe")
        vaciado = input(
            "¿Quieres hacerle un vaciado de seguridad,(Responde usando mayusculas)")
        if vaciado == 'SI':
            arcpy.env.workspace = mi_gdb
            featureclasses_existentes = arcpy.ListFeatureClasses()
            for featureClass in featureclasses_existentes:
                arcpy.management.DeleteFeatures(featureClass)
        elif vaciado == 'NO':
            adjuntarCapas = input(
                "¿Quieres añadir capas a la .gdb desde tu carpeta de datos oiriginal? ,(Responde usando mayusculas)")
            if adjuntarCapas == 'SI':
                arcpy.env.workspace = carpeta_datos_shp
                featureclasses = arcpy.ListFeatureClasses()

                for index, feature in enumerate(featureclasses):
                    print(f'[{index}] {feature} ')

                indices_capas = input(
                    'Introduce los índices de las capas que quieres usar, separados por comas: ')
                indices_capas_uso = [int(indice.strip())
                                     for indice in indices_capas.split(',')]

                
                lista_path = []
                for indice in indices_capas_uso:
                    capa = featureclasses[indice].replace('.shp', '')
                    control = os.path.basename(capa)
                    control = control.replace('(', '_').replace(')', '_')
                    out_featureclass = os.path.join(mi_gdb, control)
                    lista_path.append(out_featureclass)
                    print(lista_path[-1])
                    arcpy.management.CopyFeatures(capa, out_featureclass)

                print("Elementos copiados en la gdb")
            elif adjuntarCapas == 'NO':
                pass
    else:
        print("Tu gdb no existe")
        input_new_gdb = input("Introduce la ruta de la GDB  que vas a crear: ")
        new_gdb = input_new_gdb
        print(new_gdb)
        input_name_gdb = input(
            "Introduce el nombre de la GDB que vas a crear: ")
        new_name = "{}.gdb".format(input_name_gdb)
        print(new_name)
        arcpy.management.CreateFileGDB(new_gdb, new_name)
        print("Se ha creado una .gdb con el nombre: {}".format(input_name_gdb))

        arcpy.env.workspace = carpeta_datos_shp
        featureclasses = arcpy.ListFeatureClasses()

        for index, feature in enumerate(featureclasses):
            print(f'[{index}] {feature} ')

        indices_capas = input(
            'Introduce los índices de las capas que quieres usar, separados por comas: ')
        indices_capas_uso = [int(indice.strip())
                             for indice in indices_capas.split(',')]

        lista_path = []
        for indice in indices_capas_uso:
            capa = featureclasses[indice].replace('.shp', '')
            control = os.path.basename(capa)
            control = control.replace(
                '(', '_').replace(')', '_').replace('-', '_')
            out_featureclass = os.path.join(mi_gdb, control)
            lista_path.append(out_featureclass)
            print(lista_path[-1])
            arcpy.management.CopyFeatures(capa, out_featureclass)

        print("Capas vectoriales copiadas en la gdb")

    # Momento de evaluar la presencia de rasters en la carpeta de datos
    arcpy.env.workspace = ruta_datos
    nombreGDB=os.path.join(ruta_datos,"{}.gdb".format(nombre_gdb))
    print("Evaluemos los rasters")
    rasters = arcpy.ListRasters("*", "All")
    print(rasters)
    if len(rasters)==0:
        print("No tienes rasters en tu carpeta")
    elif len(rasters)==1:
        print("Solo hay un raster:{}".format(rasters))
        pregunta1raster= input("Quieres introducir {} en la gdb? ".format(rasters))
        if pregunta1raster == "SI":
            for raster in rasters:
                arcpy.env.workspace = nombreGDB
                raster_obj = arcpy.Raster(raster)
                arcpy.conversion.RasterToGeodatabase("{}".format(raster), "{}.gdb".format(nombre_gdb))
                print("Raster importado a la gdb")
        else:
            pass

    elif len(rasters)>1:
        indices_raster = input(
            'Introduce los índices de los raster que quieres usar, separados por comas: ')
        indices_rasters_uso = [int(indice.strip())
                             for indice in indices_raster.split(',')]
        rasters_string = ";".join(indices_rasters_uso)
        arcpy.conversion.RasterToGeodatabase(rasters_string, nombre_gdb)


config = gestionar_gdb(r"C:\Users\usuario\Documents\ArcGIS\Projects\Pythoneo\Data\BTN", "Colomera")
