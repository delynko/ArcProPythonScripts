import arcpy

project = arcpy.mp.ArcGISProject(r'Q:\ForTesting\ForTesting.aprx')
merp = project.listMaps()[0]
for l in merp.listLayers():
    print(l.name)