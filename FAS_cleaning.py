import arcpy

fc = r'P:\Projects\animal_control\data\FoothillsAnimalShelter\Clean\FAS_Clean.gdb\FAS_Geocode_Clean'
singleIdFc = r'P:\Projects\animal_control\data\FoothillsAnimalShelter\Processing\FoothillsAnimalShelter_Processing.gdb\FAS_SinglePetId'

arcpy.MakeFeatureLayer_management(fc, "selectionLayer")

rowCount = int(arcpy.GetCount_management(fc).getOutput(0))

curs = arcpy.SearchCursor(fc, ["*"])

x = 1
petId = []

for row in curs:
	pid = row.getValue("USER_Pet_ID")
	objId = row.getValue("OBJECTID")
	if pid in petId:
		print(str(pid) + " already in list. " + str(rowCount - x) + " more to go")
		x += 1
	elif pid not in petId:
		qry = "OBJECTID = {}".format(objId)
		arcpy.SelectLayerByAttribute_management("selectionLayer", "ADD_TO_SELECTION", qry)
		petId.append(pid)
		x += 1
		print(str(rowCount - x) + " more to go")

print("Appending selection to new feature class.")
arcpy.Append_management("selectionLayer", singleIdFc)

arcpy.Delete_management("selectionLayer")

# table = r'P:/Projects/animal_control/data/FoothillsAnimalShelter/Processing/FoothillsAnimalShelter_Processing.gdb/FAS'
# streets = r'C:/Users/edelynko/AppData/Roaming/ESRI/Desktop10.4/ArcCatalog/edelynko as edelynko to Warehouse.sde/JEFFCO.Transportation/JEFFCO.Street'
# street_type = r'C:/Users/edelynko/AppData/Roaming/ESRI/Desktop10.4/ArcCatalog/edelynko as edelynko to Warehouse.sde/JEFFCO.StreetType'
#
# streetNames = []
# streetCurs = arcpy.SearchCursor(streets, ["STREET_NAME"])
# for row in streetCurs:
# 	streetNames.append(row.getValue("STREET_NAME"))
#
# streetNames.sort()
# print(streetNames)
#
# fasCursor = arcpy.SearchCursor(table, ["St_Name"])
#
# x = 0
# notAStreet = []
# for row in fasCursor:
# 	name = row.getValue("St_Name")
# 	if name not in streetNames:
# 		if name not in notAStreet:
# 			notAStreet.append(name)
# 			x += 1
#
# notAStreet.sort()
# for n in notAStreet:
# 	print(n + " is not a Jeffco street")
# print(x)

# fullAddr(!St_Num!,!St_Dir!,!St_Name!,!St_Type!)


# def fullAddr(num,dir,name,type):
#     if dir is none:
#         d = ''
#     else:
#         d = dir
#     if type is none:
#         t = ''
#     else:
#         t = type
#     return str(num) + " " + d + " " + name + " " + t




# addresses = 'C:/Users/edelynko/AppData/Roaming/ESRI/Desktop10.4/ArcCatalog/edelynko as edelynko to Warehouse.sde/JEFFCO.Address/JEFFCO.MasterAddress'
#
# addrCurs = arcpy.SearchCursor(addresses, ["*"])
#
# street_numbers = []
# for row in addrCurs:
# 	street_numbers.append(str(row.getValue("ADRHSNO")))
#
# print("Finished obtaining all address numbers")
#
# curs = arcpy.UpdateCursor(table)
#
# for row in curs:
# 	if str(row.getValue("St_Num")) in street_numbers:
# 		print(str(row.getValue("St_Num")) + " is an Address Number")
# 	else:
# 		curs.deleteRow(row)
#
