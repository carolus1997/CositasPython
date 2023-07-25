import arcpy,os
from arcpy.sa import *
arcpy.env.overwriteOutput = True
inputDatos= input("Introduce la ruta de tu carpeta de datos con los que vas a trabajar: ")
carpetaDatosSHP = inputDatos
# print(carpetaDatosSHP)
inputGDB= input("Introduce el nombre de tu GDB con la que vas a trabajar: ")
miGDB = os.path.join(carpetaDatosSHP, "{}.gdb".format(inputGDB))
print(miGDB)
### Creando una GDB ###
if  arcpy.Exists(miGDB):
    print("Tu gdb ya existe, vamos a hacerle un vaciado de seguridad")
    ### Vaciado de seguridad de la gdb###
    arcpy.env.workspace = miGDB
    featureclassesExistentes = arcpy.ListFeatureClasses()
    for featureClass in featureclassesExistentes:
        arcpy.management.DeleteFeatures(featureClass)
else:
    print("Tu gdb no existe")
    inputNewGDB= input("Introduce la ruta de la GDB  que vas a crear: ")
    newGDB = inputNewGDB
    print(newGDB)
    inpuntNameGDB=input("Introduce el nombre de la GDB que vas a crear: ")
    newName= "{}.gdb".format(inpuntNameGDB)
    print(newName)
    arcpy.management.CreateFileGDB(newGDB,newName)

    print("Se ha creado una .gdb con el nombre: {}".format(inpuntNameGDB))

### Configurando el espacio de trabajo ###
arcpy.env.workspace = carpetaDatosSHP
featureclasses = arcpy.ListFeatureClasses()

# Imprimir todas las capas disponibles con su índice
for index, feature in enumerate(featureclasses):
    print(f'[{index}] {feature} ')

# Pedir al usuario que ingrese los índices de las capas que quiere utilizar
indices_capas_uso = input("Introduce los índices de las capas que quieres utilizar, separados por comas: ")

# Convertir la entrada del usuario en una lista de índices
indices_capas_uso = [int(indice.strip()) for indice in indices_capas_uso.split(',')]

# Seleccionar e importar capas en la GDB de acuerdo a los índices proporcionados por el usuario
listaNames=[]
listaPath = []
for indice in indices_capas_uso:
    capa = featureclasses[indice].replace('.shp', '')
    # Reemplazar los paréntesis por guiones bajos en el nombre de la capa
    control = os.path.basename(capa)
    control = control.replace('(', '_').replace(')', '_')
    out_featureclass = os.path.join(miGDB, control)
    listaPath.append(out_featureclass)
    print(listaPath[-1])
    arcpy.management.CopyFeatures(capa, out_featureclass)

print("Elementos copiados en la gdb")