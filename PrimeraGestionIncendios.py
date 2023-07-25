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

