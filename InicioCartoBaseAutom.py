import arcpy, os
from arcpy.sa import *

arcpy.env.overwriteOutput = True

miGDB = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\CartoBase.gdb"
carpetaDatosSHP = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Escritorio\Docu\Cursos\PYTS_Scripts de geoprocesamiento con Python en ArcGIS Pro\Inglés\Student"

# ### Vaciado de seguridad de la gdb###
# arcpy.env.workspace = miGDB
# featureclassesExistentes = arcpy.ListFeatureClasses()
# for featureClass in featureclassesExistentes:
#     arcpy.management.DeleteFeatures(featureClass)

### Creando una GDB ###
if miGDB in locals():
    ### Vaciado de seguridad de la gdb###
    arcpy.env.workspace = miGDB
    featureclassesExistentes = arcpy.ListFeatureClasses()
    for featureClass in featureclassesExistentes:
        arcpy.management.DeleteFeatures(featureClass)
else:
    arcpy.management.CreateFileGDB(
        r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos",
        "cartoBase.gdb")

### Configurando el espacio de trabajo ###
arcpy.env.workspace = carpetaDatosSHP
featureclasses = arcpy.ListFeatureClasses()
for feature in featureclasses:
    print([feature, featureclasses.index(feature)])

### Seleccionar e importar capas en la GDB ###
listaCapasUso = [featureclasses[0], featureclasses[1], featureclasses[11], featureclasses[29], featureclasses[33],
                 featureclasses[34],
                 featureclasses[35]]

listaPath = []
for capa in listaCapasUso:
    capa = capa.replace('.shp', '')
    control = os.path.basename(capa)
    out_featureclass = os.path.join(miGDB, os.path.basename(capa))
    listaPath.append(out_featureclass)
    arcpy.management.CopyFeatures(capa, out_featureclass)

print("Elementos copiados en la gdb")

###Reconfiguramos el espacio de trabajo###
arcpy.env.workspace = miGDB  # a partir de ahora usamos la gdb
featureclassesGDB = arcpy.ListFeatureClasses()

###Obtener la informacion necesaria para crear los puntos nuevos###
capaUrbana = 'BTN0622L_URBANA'
fields = ['ID', 'SHAPE@']
listaCoords=[]
if capaUrbana in featureclassesGDB: #buscamos la capa urbana en la gdb
    with arcpy.da.SearchCursor(capaUrbana, fields) as cursor: #empezamos a buscar en la capa, los campos que hemos puesto
        for row in cursor: #nos metemos en la lista que nos da al buscar lo que le pedimos
            coordX = row[1].lastPoint.X #Nos quedamos con la coordenada X del ultimo vertice de cada linea
            coordY = row[1].lastPoint.Y #Nos quedamos con la coordenada Y del ultimo vertice de cada linea
            ID = row[0] #Nos quedamos con el ID del ultimo vertice de cada linea
            listaCoords.append(((coordX,coordY),ID)) #lo metemos todo en una lista que nos sirva para posteriores analisis con el formato correcto para las coordenadas

### Creamos la capa de puntos VACIA###
fields = ['ID','SHAPE@XY']
out_path= miGDB
out_name= "PuntosFinales"
geometry_type='POINT'
spatial_reference=25830
arcpy.management.CreateFeatureclass(out_path, out_name, geometry_type, "", "", "", spatial_reference)
print("Capa de puntos creada")

### Poblar la capa de Puntos VACIA ###
arcpy.management.AddField(out_name, 'ID','FLOAT')
print("Campo ID creado")
fields = ['SHAPE@XY', 'ID']
cursor = arcpy.da.InsertCursor(out_name,fields)
for row in listaCoords:
    cursor.insertRow(row)
print("Registros Añadidos")



########################################################################### PARTE 2 #######################################################
arcpy.sa.TopoToRaster('BTN0201L_CUR_NIV', "15")
# DEM= TopoToRaster('BTN0201L_CUR_NIV',"15")
# DEM.save(os.path.join(miGDB + "DEM1.tif"))
print("DEM Listo")