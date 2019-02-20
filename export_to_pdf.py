import arcpy

aprx = arcpy.mp.ArcGISProject(r"\\admin.co.jeffco.us\files\Groups\Parks\OS\GIS\2_Teams\2_6_Rangers\Team_Projects\2018\20180101_Emergency_Resource_Atlas\GIS\ArcPro\Emergency_Resource_Atlas.aprx")
lyts = aprx.listLayouts()

for lyt in lyts:
    if lyt.name.startswith("_") == False:
        print(lyt.name)
        lyt.exportToPDF(r"\\admin.co.jeffco.us\files\Groups\Parks\OS\GIS\2_Teams\2_6_Rangers\Team_Projects\2018\20180101_Emergency_Resource_Atlas\GIS\ArcPro\Exports\{}.pdf".format(lyt.name), resolution=300)
