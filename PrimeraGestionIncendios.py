import arcpy,os
# Esta función permite, con una ruta y un nombre de una gdb, poder gestionar de primeras la creación y población de una gdb si la necesitamos
def gestionar_gdb(ruta_datos, nombre_gdb):
    carpeta_datos_shp = ruta_datos
    mi_gdb = os.path.join(carpeta_datos_shp, "{}.gdb".format(nombre_gdb))
    print(mi_gdb)

    if arcpy.Exists(mi_gdb):
        print("Tu gdb ya existe")
        vaciado = input("¿Quieres hacerle un vaciado de seguridad,(Responde usando mayusculas)")
        if vaciado == 'SI':
            arcpy.env.workspace = mi_gdb
            featureclasses_existentes = arcpy.ListFeatureClasses()
            for featureClass in featureclasses_existentes:
                arcpy.management.DeleteFeatures(featureClass)
        elif vaciado == 'NO':
            adjuntarCapas= input("¿Quieres añadir capas a la .gdb desde tu carpeta de datos oiriginal? ,(Responde usando mayusculas)")
            if adjuntarCapas == 'SI':
                arcpy.env.workspace = carpeta_datos_shp
                featureclasses = arcpy.ListFeatureClasses()

                for index, feature in enumerate(featureclasses):
                    print(f'[{index}] {feature} ')

                indices_capas = input('Introduce los índices de las capas que quieres usar, separados por comas: ')
                indices_capas_uso = [int(indice.strip()) for indice in indices_capas.split(',')]

                lista_names = []
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
            elif adjuntarCapas=='NO':
                pass
    else:
        print("Tu gdb no existe")
        input_new_gdb = input("Introduce la ruta de la GDB  que vas a crear: ")
        new_gdb = input_new_gdb
        print(new_gdb)
        input_name_gdb = input("Introduce el nombre de la GDB que vas a crear: ")
        new_name = "{}.gdb".format(input_name_gdb)
        print(new_name)
        arcpy.management.CreateFileGDB(new_gdb, new_name)
        print("Se ha creado una .gdb con el nombre: {}".format(input_name_gdb))

        arcpy.env.workspace = carpeta_datos_shp
        featureclasses = arcpy.ListFeatureClasses()

        for index, feature in enumerate(featureclasses):
            print(f'[{index}] {feature} ')

        indices_capas = input('Introduce los índices de las capas que quieres usar, separados por comas: ')
        indices_capas_uso = [int(indice.strip()) for indice in indices_capas.split(',')]

        lista_path = []
        for indice in indices_capas_uso:
            capa = featureclasses[indice].replace('.shp', '')
            control = os.path.basename(capa)
            control = control.replace('(', '_').replace(')', '_').replace('-', '_')
            out_featureclass = os.path.join(mi_gdb, control)
            lista_path.append(out_featureclass)
            print(lista_path[-1])
            arcpy.management.CopyFeatures(capa, out_featureclass)

        print("Elementos copiados en la gdb")


config = gestionar_gdb(r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\CurvasNivel","CurvasNivelPruebaDEM")