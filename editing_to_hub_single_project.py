import arcpy

project = r'\\admin.co.jeffco.us\files\Groups\Parks\OS\GIS\2_Teams\2_6_Rangers\Team_Projects\2018\20180101_Emergency_Resource_Atlas\GIS\ArcPro\Emergency_Resource_Atlas.aprx'

editingGDB = r'\\admin\Admin\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data___EDITING.gdb'
hubGDB = r'\\admin\Admin\Groups\Parks\OS\GIS\1_GIS_Hub\1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data.gdb'

aprx = arcpy.mp.ArcGISProject(project)

aprx.updateConnectionProperties(editingGDB, hubGDB)