import arcpy
import time
import datetime
from datetime import timedelta

acFc = r'P:\Projects\animal_control\AnimalControl\AnimalControl.gdb\AnimalControl'



lpTable = r'P:\Projects\animal_control\AnimalControl\AnimalControl.gdb\LunarPhase'

before = timedelta(days=2)
after = timedelta(days=-2)

moonCurs = arcpy.SearchCursor(lpTable, ["*"])

phaseDates = []

for row in moonCurs:
	date = row.getValue("date")
	startDate = date - before
	endDate = date - after

	if row.getValue("phase") == "Full Moon":
		fm = {
			'moonPhase': "Full Moon",
			'dateRange': {
				"startDate": startDate,
				"endDate": endDate
			}
		}
		phaseDates.append(fm)

	if row.getValue("phase") == "New Moon":
		nm = {
			'moonPhase': "New Moon",
			'dateRange': {
				"startDate": startDate,
				"endDate": endDate
			}
		}

		phaseDates.append(nm)

x = 0
newMoonObjIds = []
print(len(phaseDates))
for p in phaseDates:
	if p['moonPhase'] == 'Full Moon':
		sd = p['dateRange']['startDate']
		ed = p['dateRange']['endDate']

		newLayer = arcpy.MakeFeatureLayer_management(acFc, "acLayer")

		acCurs = arcpy.SearchCursor("acLayer", ["*"])

		for row in acCurs:
			if row.getValue("INCIDENT_TYPE") == 'BARK':
				date = row.getValue("DATE")
				if sd <= date <= ed:
					newMoonObjIds.append(row.getValue("OBJECTID"))
		x += 1
		print(str(len(phaseDates) - x) + " to go.")

		arcpy.Delete_management("acLayer")
		print(newMoonObjIds)

print(newMoonObjIds)
