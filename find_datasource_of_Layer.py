import arcpy

editingGDB = r'\\admin\Admin\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data___EDITING.gdb'

project = arcpy.mp.ArcGISProject(r"\\admin.co.jeffco.us\files\Groups\Parks\OS\GIS\2_Teams\2_6_Rangers\Team_Projects\2018\20180101_Emergency_Resource_Atlas\GIS\ArcPro\Emergency_Resource_Atlas.aprx")

maps = project.listMaps()

for m in maps:
    print(m.name)
    layers = m.listLayers()
    for l in layers:
        if l.supports("DATASOURCE"):
            print("\tSource: {}; Layer: {}".format(l.dataSource.replace("\\admin.co.jeffco.us\\files\Groups\Parks\OS", ""), l.name))
