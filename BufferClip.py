import arcpy, os
from arcpy.sa import *

### SET THE WORKSPACE ###

arcpy.env.workspace = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Documentos\ArcGIS\Projects\Demos_Cursos\PYTS.gdb"
arcpy.env.overwriteOutput = True

### ACCESO A LAS CAPAS ###

carreterasFC = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Escritorio\Docu\Cursos\PYTS_Scripts de geoprocesamiento con Python en ArcGIS Pro\Inglés\Student\BTN0302L_RIO"
riosFC = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Escritorio\Docu\Cursos\PYTS_Scripts de geoprocesamiento con Python en ArcGIS Pro\Inglés\Student\BTN0605L_CARRETERA"
edificiosFC = r"C:\Users\carlos.mira-perceval\OneDrive - ESRI ESPAÑA Soluciones Geoespaciales S.L\Escritorio\Docu\Cursos\PYTS_Scripts de geoprocesamiento con Python en ArcGIS Pro\Inglés\Student\BTN0507S_EDIFIC"

### COPY FEATURES IN GDB ###

listaCapasImportar = [carreterasFC, riosFC, edificiosFC]
listaPath = []
for capa in listaCapasImportar:
    control = os.path.basename(capa)
    out_featureclass = os.path.join(arcpy.env.workspace, os.path.basename(capa))
    listaPath.append(out_featureclass)
    arcpy.management.CopyFeatures(capa, out_featureclass)

print("Elementos copiados en la gdb")

### ACCEDER A LA GDB ###

featureClasses = arcpy.ListFeatureClasses()  # genera una lista
# print(featureClasses)

### INTERSECAR LAS CARRETERAS CON RIOS ####

inFeatures = ["BTN0302L_RIO", "BTN0605L_CARRETERA"]
intersectOutput = "ZonasCruce"
arcpy.analysis.Intersect(inFeatures, intersectOutput, "", "", "point")

### CREAR UN BUFFER A PARTIR DE LOS PUNTOS DE CRUCE ###
in_features = intersectOutput
out_feature_class = "BuffersPuntosCruce500m"
buffer_distance_or_field = "500 meters"

arcpy.analysis.Buffer(in_features, out_feature_class, buffer_distance_or_field)

print("Ya se han creado los buffers")

### RECORTAR LOS EDIFICIOS QUE ESTÉN DENTRO DEL BUFFER ###

in_features_Clip = 'BTN0507S_EDIFIC'
clip_features_Clip = out_feature_class
out_feature_class_Clip = "ZonasPeligro"
arcpy.analysis.Clip(in_features_Clip, clip_features_Clip, out_feature_class_Clip)

###Edificios a centroides###
in_features_Centroid=out_feature_class_Clip
out_feature_class_Centroid= "CentroidesEdificios"
arcpy.management.FeatureToPoint(in_features_Centroid, out_feature_class_Centroid, 'CENTROID')

###VISUALIZACION EN DENSIDAD ###
in_features_KernelD= out_feature_class_Centroid
population_field_KernelD= 'None'
cellSize = 60
KernelDensity(in_features_KernelD, population_field_KernelD, cellSize)

print("Edificios Recortados")
print("Script Terminado")