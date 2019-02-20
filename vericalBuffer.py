import arcpy
from arcpy.sa import *
import os

pointFC = r"Q:\arcpy-scripts\VerticleBufferScript\New File Geodatabase.gdb\test_point"
origDEM = r"Q:\arcpy-scripts\VerticleBufferScript\New File Geodatabase.gdb\zion_dem_utm12"
elevDiff = 25

arcpy.InterpolateShape_3d(origDEM, pointFC, os.path.join(pointFC + "_3d"))

interpShapeFC = r"Q:\arcpy-scripts\VerticleBufferScript\New File Geodatabase.gdb\test_point_3d"

arcpy.AddField_management(interpShapeFC, "BufferZ", "DOUBLE")

zCurs = arcpy.UpdateCursor(interpShapeFC, ["SHAPE", "BufferZ"])

for row in zCurs:
	print(row.getValue("name") + " " + str(row.getValue("SHAPE").getPart().Z))
	elev = row.getValue("SHAPE").getPart().Z + elevDiff
	row.setValue("BufferZ", elev)
	zCurs.updateRow(row)
