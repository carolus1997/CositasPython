import arcpy
import os
from arcpy.sa import *
from arcpy import env
arcpy.env.overwriteOutput = True
# Esta función permite, con una ruta y un nombre de una gdb, poder gestionar de primeras la creación y población de una gdb si la necesitamos


def gestionar_gdb(ruta_datos, nombre_gdb):
    carpeta_datos_shp = ruta_datos
    mi_gdb = os.path.join(carpeta_datos_shp, "{}.gdb".format(nombre_gdb))
    print(mi_gdb)
    arcpy.env.overwriteOutput = True
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
    nombreGDB = "{}.gdb".format(nombre_gdb)
    print("Evaluemos los rasters")
    rasters = arcpy.ListRasters("*", "All")
    print(rasters)
    if len(rasters) == 0:
        print("No tienes rasters en tu carpeta")
    elif len(rasters) == 1:
        print("Solo hay un raster:{}".format(rasters))
        pregunta1raster = input(
            "Quieres introducir {} en la gdb? ".format(rasters))
        if pregunta1raster == "SI":
            for raster in rasters:
                raster_obj = "{}".format(raster)
                arcpy.conversion.RasterToGeodatabase(
                    raster_obj, "{}.gdb".format(nombre_gdb))
                print("Raster importado a la gdb")
        else:
            pass
    elif len(rasters) > 1:
        print("En tu carpeta de datos hay {} rasters, y son:{}".format(
            len(rasters), rasters))
        pregunta2raster = input("Quieres introducir algun raster en la gdb? ")
        if pregunta2raster == "SI":
            for index, feature in enumerate(rasters):
                print(f'[{index}] {feature} ')
            indices_raster = input(
                'Introduce los índices de los raster que quieres usar, separados por comas: ')
            indices_rasters_uso = [int(indice.strip())
                                   for indice in indices_raster.split(',')]
            # Recogemos los rasters correspondientes a los índices.
            rasters_uso = [rasters[indice] for indice in indices_rasters_uso]
            # Unimos los nombres de los rasters con ";"
            rasters_string = ";".join(rasters_uso)
            print(rasters_string)
            arcpy.conversion.RasterToGeodatabase("{}".format(rasters_string), "{}.gdb".format(nombre_gdb))

    #CARTORASTER BASE
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
        output_layer = os.path.join(mi_gdb,"CurvasNivelTotal") # Cambia esto a la ruta de salida que desees
        arcpy.Merge_management(layers_to_merge, output_layer)
        print("Curvas de nivel combinadas")
    else:
        output_layer = os.path.join(mi_gdb, "CurvasNivelTotal")
        print("Solo hay una capa")

    indices_campos_uso=[]
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
        output_dem_path = os.path.join(mi_gdb, output_dem_name)
        DEM.save(os.path.join(ruta_datos,"{}.tif".format(output_dem_name)))

    # Una vez creado el DEM, creamos el Hillshade y Slope
    # Hillshade
    arcpy.env.workspace = ruta_datos
    rasters = arcpy.ListRasters("*", "All")
    for raster in rasters:
        print(raster)
        outHillshade = Hillshade(raster)
        outHillshade.save(os.path.join(ruta_datos, "Hillshade.tif"))
        print("Hillshade Generado")

        # Slope
        outSlope = Slope(raster, "DEGREE")
        outSlope.save(os.path.join(ruta_datos, "Slope.img"))
        print("Slope Generado")
    rasters = arcpy.ListRasters("*", "All")
    rasters_string = ";".join(rasters)
    print("La lista de rasters a importar es: {}".format(rasters_string))
    arcpy.conversion.RasterToGeodatabase("{}".format(rasters_string), "{}.gdb".format(nombre_gdb))

    # Momento de evaluar la presencia de rasters no proyectados en la gdb
    arcpy.env.workspace = mi_gdb

    # rasters con sistema de coordenadas
    rasters_with_coordinates = []

    # Rasters sin un sistema de coordenadas
    rasters_without_coordinates = []

    # Lista de los nombres de los rasters en la geodatabase
    raster_list = arcpy.ListRasters()

    for raster in raster_list:
        # Obtiene el spatialReference del raster actual
        raster_sr = arcpy.Describe(raster).spatialReference

        if raster_sr.name == 'Unknown':
            # Agregar el raster a la lista de rasters sin un sistema de coordenadas
            rasters_without_coordinates.append(raster)
        else:
            # Agregar el raster a la lista de rasters con un sistema de coordenadas
            rasters_with_coordinates.append(raster)


    # Comif we didn't find any raster with coordinates, print a message and exit
    if len(rasters_with_coordinates) == 0:
        print("No se encontró ningún raster con un sistema de coordenadas.")
        return


    # Sistema de coordenadas del primer raster que tiene uno
    spatial_ref = arcpy.Describe(rasters_with_coordinates[0]).spatialReference

    # Si solo hay un raster sin un sistema de coordenadas, se lo proyectamos
    if len(rasters_without_coordinates) == 1:
        out_raster = rasters_without_coordinates[0] + "_projected"
        arcpy.DefineProjection_management(rasters_without_coordinates[0], spatial_ref)
    elif len(rasters_without_coordinates) > 1:
        for raster in rasters_without_coordinates:
            out_raster = raster + "_projected"
            arcpy.DefineProjection_management(raster, spatial_ref)
    
    print("Procesamiento completado.")


config = gestionar_gdb(
    r"C:\Users\usuario\Documents\ArcGIS\Projects\Pythoneo\Data\BTN", "Colomera")
 


