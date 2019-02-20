import arcpy
from arcpy.sa import *

fc = "PolyAlloc"
fcCount = arcpy.GetCount_management("PolyAlloc")
demInt = "DEM_INT"
md = r"Q:/ForTesting/Euclidean.gdb/AdjustedFloodPlain"

arcpy.MakeFeatureLayer_management(fc, "fl")

polyCurs = arcpy.SearchCursor("fl", ["*"])

x = 1
for row in polyCurs:
    elev = row.getValue("gridcode")
    objID = row.getValue("OBJECTID")
    print("Selecting feature")
    arcpy.SelectLayerByAttribute_management("fl", "NEW_SELECTION", "OBJECTID = {}".format(objID))
    print("Creating shapefile from feature")
    arcpy.CopyFeatures_management("fl", "Q:/ForTesting/Euclid/temp.shp")
    print("Assigning mask")
    arcpy.env.mask = "Q:/ForTesting/Euclid/temp.shp"
    print("Creating new raster based on elevation")
    outCon = Con(demInt, 0, 1, "Value > {}".format(elev + 15))
    print("Saving raster")
    outCon.save("Q:/ForTesting/Euclid/outCon{}.img".format(x))
    print("Adding new raster to Mosaic Dataset")
    arcpy.AddRastersToMosaicDataset_management(md, "Raster Dataset", "Q:/ForTesting/Euclid/outCon{}.img".format(x))
    print("Deleting shapefile")
    arcpy.Delete_management("Q:/ForTesting/Euclid/temp.shp")
    print(str(x) + " down. {} to go.".format(str(int(fcCount[0]) - x)))
    x = x + 1