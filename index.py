import arcpy
import os

arcpy.env.overwriteOutput = True

BASE_DIR = os.path.dirname(__file__)

# arcpy.env.workspace = BASE_DIR


DATA_MCA_DIR = os.path.join(BASE_DIR, 'data_mca')
TEMP_FOLDER = os.path.join(DATA_MCA_DIR, 'temp')

cuencas = os.path.join(DATA_MCA_DIR, 'cuencas.shp')
canal = os.path.join(DATA_MCA_DIR, 'canal.shp')
densidad_poblacional = os.path.join(DATA_MCA_DIR, 'densidad_poblacional.shp')
emergencias = os.path.join(DATA_MCA_DIR, 'emergencias.shp')
inundacion_erosion = os.path.join(DATA_MCA_DIR, 'inundacion_erosion.shp')
movimientos_en_masa = os.path.join(DATA_MCA_DIR, 'movimientos_en_masa.shp')
punto_critico = os.path.join(DATA_MCA_DIR, 'punto_critico.shp')
presas = os.path.join(DATA_MCA_DIR, 'presas.shp')
puentes = os.path.join(DATA_MCA_DIR, 'puentes.shp')
zonas_riesgo_no_mitigable = os.path.join(DATA_MCA_DIR, 'zonas_riesgo_no_mitigable.shp')
red_vial = os.path.join(DATA_MCA_DIR, 'red_vial.shp')
zona_urbana = os.path.join(DATA_MCA_DIR, 'zona_urbana.shp')

# Hidraulica
# C1: Distancias a infraestructura Hidraulica

def canal_proceso(canal):
    influencia = "2000 METERS"
    output = os.path.join(TEMP_FOLDER, 'canal_buffer.shp')
    arcpy.Buffer_analysis(canal, output, influencia, 'FULL', 'ROUND', 'ALL')
    return output

def presas_proceso(presas):
    influencia = "10 KILOMETERS"
    output = os.path.join(TEMP_FOLDER, 'presas_buffer.shp')
    arcpy.Buffer_analysis(presas, output, influencia, 'FULL', 'ROUND', 'ALL')
    return output

# C2: Seccion del rio a medir

def seccion_rio_proceso(red_hidrica):
    influencia = "200 METERS"
    output = os.path.join(TEMP_FOLDER, 'seccion_rio_buffer.shp')
    arcpy.Buffer_analysis(red_hidrica, output, influencia, 'FULL', 'ROUND', 'ALL')
    return output


# Seguridad
# C3: Cercania a centros poblados

def cercania_ccpp_proceso(centros_poblados):
    influencias = [1, 2, 3, 4]
    output = os.path.join(TEMP_FOLDER, 'centros_poblados_buffer.shp')
    arcpy.MultipleRingBuffer_analysis(centros_poblados, output, influencias, 'KILOMETERS', 'distance', 'ALL')
    arcpy.AddField_management(output, 'c_ccpp', 'DOUBLE')
    with arcpy.da.UpdateCursor(output, ['distance', 'c_ccpp']) as cursor:
        for row in cursor:
            row[1] = (row[0] - min(influencias))/(max(influencias) - min(influencias))
            cursor.updateRow(row)
    return output

# Accesibilidad
# C4: Horas de viaje
# C5: Calidad de acceso

def tiempo_acceso_estaciones_proceso():
    pass


# Utilidad
# C6: Uso adicional de los datos para temas distintos al de origen (susceptibilidad, alerta temprana)

def utilidad_proceso(utilidad):
    output = os.path.join(TEMP_FOLDER, 'utilidad.shp')
    arcpy.CopyFeatures_management(utilidad, output)
    return output




def densidad_poblacional_proceso(densidad_poblacional):
    scursor = [x[0] for x in arcpy.da.SearchCursor(densidad_poblacional, ['pob17_d'])]
    arcpy.AddField_management(densidad_poblacional, 'c_dp', 'DOUBLE')
    with arcpy.da.UpdateCursor(densidad_poblacional, ['c_dp', 'pob17_d']) as cursor:
        for row in cursor:
            # print(max(scursor), min(scursor))
            row[0] = (row[1] - min(scursor))/(max(scursor) - min(scursor))
            cursor.updateRow(row)
    output = os.path.join(TEMP_FOLDER, 'densidad_poblacional.shp')
    arcpy.CopyFeatures_management(densidad_poblacional, output)
    return densidad_poblacional


def emergencias_proceso(emergencias):
    pass
    

def inundacion_erosion_proceso(inundacion_erosion):
    output = os.path.join(TEMP_FOLDER, 'inundacion_erosion.shp')
    arcpy.CopyFeatures_management(inundacion_erosion, output)
    arcpy.AddField_management(output, "c_sie", "DOUBLE")
    arcpy.CalculateField_management(output, "c_sie", "(!GRIDCODE! - 1)/(4)", "PYTHON_9.3")
    return output

def movimientos_en_masa_proceso(movimientos_en_masa):
    output = os.path.join(TEMP_FOLDER, 'movimientos_en_masa.shp')
    arcpy.CopyFeatures_management(movimientos_en_masa, output)
    arcpy.AddField_management(output, "c_smm", "DOUBLE")
    arcpy.CalculateField_management(output, "c_smm", "(!GRIDCODE! - 1)/(4)", "PYTHON_9.3")
    return output

def punto_critico_proceso(punto_critico):
    influencia = "1 KILOMETERS"
    output = os.path.join(TEMP_FOLDER, 'punto_critico_buffer.shp')
    arcpy.Buffer_analysis(punto_critico, output, influencia, 'FULL', 'ROUND', 'ALL')
    return output



def puentes_proceso(puentes):
    influencia = "500 METERS"
    output = os.path.join(TEMP_FOLDER, 'puentes_buffer.shp')
    arcpy.Buffer_analysis(puentes, output, influencia, 'FULL', 'ROUND', 'ALL')
    return output

def zonas_riesgo_no_mitigable_proceso(zonas_riesgo_no_mitigable):
    output = os.path.join(TEMP_FOLDER, 'zonas_riesgo_no_mitigable.shp')
    arcpy.CopyFeatures_management(zonas_riesgo_no_mitigable, output)
    return output

def red_vial_proceso(red_vial):
    influencias = [1, 2, 3, 4, 5]
    # influencias_str = ";".join(map(lambda i: str(i), influencias))
    output = os.path.join(TEMP_FOLDER, 'red_vial_buffer.shp')
    arcpy.MultipleRingBuffer_analysis(red_vial, output, influencias, 'KILOMETERS', 'distance', 'ALL')
    arcpy.AddField_management(output, 'c_rv', 'DOUBLE')
    with arcpy.da.UpdateCursor(output, ['distance', 'c_rv']) as cursor:
        for row in cursor:
            row[1] = (row[0] - min(influencias))/(max(influencias) - min(influencias))
            cursor.updateRow(row)
    return output

def zona_urbana_proceso(zona_urbana):
    output = os.path.join(TEMP_FOLDER, 'zona_urbana.shp')
    arcpy.CopyFeatures_management(zona_urbana, output)
    return output


def mca_por_cuenca(variable, cuenca_geometry, callback):
    arcpy.SelectLayerByLocation_management(variable, 'INTERSECT', cuenca_geometry, '', 'NEW_SELECTION')
    return callback(variable)


variables = [
    {
        'path': canal,
        'proceso': canal_proceso,
    },
    {
        'path': densidad_poblacional,
        'proceso': densidad_poblacional_proceso,
    },
    {
        'path': inundacion_erosion,
        'proceso': inundacion_erosion_proceso,
    },
    {
        'path': movimientos_en_masa,
        'proceso': movimientos_en_masa_proceso,
    },
    {
        'path': punto_critico,
        'proceso': punto_critico_proceso,
    },
    {
        'path': presas,
        'proceso': presas_proceso,
    },
    {
        'path': puentes,
        'proceso': puentes_proceso,
    },
    {
        'path': zonas_riesgo_no_mitigable,
        'proceso': zonas_riesgo_no_mitigable_proceso,
    },
    {
        'path': red_vial,
        'proceso': red_vial_proceso,
    },
    {
        'path': zona_urbana,
        'proceso': zona_urbana_proceso,
    }
]

variables_por_cuencas = dict()
arcpy.Exists(cuencas)
cursor = arcpy.da.SearchCursor(cuencas, ['CD_CUENCA', 'SHAPE@'], "CD_CUENCA = '1378'")
for i in cursor:
    print(i[0])
    row = list()
    for variable in variables:
        mfl = arcpy.MakeFeatureLayer_management(variable['path'], 'variable')
        response = mca_por_cuenca(mfl, i[1], variable['proceso'])
        row.append(response)
    variables_por_cuencas[i[0]] = row
    output_mca = os.path.join(TEMP_FOLDER, 'mca_cuenca_{}.shp'.format(i[0]))
    arcpy.Union_analysis(row, output_mca, 'ALL', '#', 'GAPS')
    # arcpy.Intersect_analysis(row, output_mca)

    for r in range(1, 11):
        name_field = 'C' + str(r).zfill(2)
        arcpy.AddField_management(output_mca, name_field, 'DOUBLE')
    break


# 1375534
# 138
# 13776
# 1378
# 132
# 137556
# 137772
# 137716
