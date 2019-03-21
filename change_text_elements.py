import arcpy

aprx = arcpy.mp.ArcGISProject(r'M:\GIS\2_Teams\2_6_Rangers\Team_Projects\2019\20190101_Emergency_Resource_Atlas\GIS\ArcPro\Emergency_Resource_Atlas.aprx')

lyts = aprx.listLayouts()

for lyt in lyts:
    print(lyt.name)
