import arcpy

zipFC = r'P:/Projects/Workforce/Workforce.gdb/ZIP_with_Counts'

jobsFC = r'P:/Projects/Workforce/Workforce.gdb/TriCountyZIPCodesWithJobs'

curs = arcpy.UpdateCursor(zipFC)

for row in curs:
	zipCode = row.getValue("ZIP")

	fakeLayer = arcpy.MakeFeatureLayer_management(jobsFC, 'fakeLayer')

	sel = arcpy.SelectLayerByAttribute_management('fakeLayer', 'NEW_SELECTION', '"Tri_County_ZIP_ZIP" = {}'.format("'" + zipCode + "'"))

	cnt = arcpy.GetCount_management(sel)

	row.setValue('Jobs', cnt)

	curs.updateRow(row)

	print(zipCode + " " + str(cnt))

	arcpy.Delete_management(fakeLayer)
