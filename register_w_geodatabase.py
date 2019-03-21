import arcpy
from arcpy import env
env.workspace = "Database Connections\os_gisanalyst@dcp-OSGDBP.sde"
fc = r"Database Connections\os_gisanalyst@dcp-OSGDBP.sde\OS_GISANALYST.LBT"
try:
    arcpy.RegisterWithGeodatabase_management(fc)
except:
    print(arcpy.GetMessages())