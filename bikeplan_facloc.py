import arcpy

curs = arcpy.UpdateCursor('bikeplan')

dir = "N"
dir2 = "S"

segments = []

for row in curs:
	loc = row.getValue('FAC_LOC')
	bluid = row.getValue('BLUID')


	if bluid not in segments:

		row.setValue("FAC_LOC", dir)
		curs.updateRow(row)

		segments.append(bluid)

	if bluid in segments:
		if row.getValue("FAC_LOC") == None:
			row.setValue("FAC_LOC", dir2)
			curs.updateRow(row)