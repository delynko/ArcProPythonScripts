import arcpy
import csv
import logging
import datetime
import time
import mailer

message = mailer.Message()
message.From = 'edelynko@co.jefferson.co.us'
message.To = ["edelynko@co.jefferson.co.us", "cxwhite@co.jefferson.co.us", "cbouchar@co.jefferson.co.us", "rthayer@co.jefferson.co.us"]

start = time.time()

todayDate = datetime.date.today()
d = str(todayDate).replace("-", "")

logFile = r"\\admin\Admin\Groups\Parks\OS\GIS_TEAM\3_Resources\3_1_GIS_Team\3_1_8_Tracking\Data_Sync_Log\{}.log".format(d)
csvFile = r'\\admin\Admin\Groups\Parks\OS\GIS_TEAM\3_Resources\3_1_GIS_Team\3_1_8_Tracking\Tracking___PRO_Data_Sourced_to_Editing_Database.csv'

editingGDB = r'\\admin\Admin\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data___EDITING.gdb'
hubGDB = r'\\admin\Admin\Groups\Parks\OS\GIS\1_GIS_Hub\1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data.gdb'

with open(csvFile, 'r') as f:
    reader = csv.reader(f)

    # Skip headers
    next(reader, None)
    for row in reader:

        if len(row) > 0:

            m = row[0].strip()

            aprx = arcpy.mp.ArcGISProject(r'{}'.format(m))

            aprx.updateConnectionProperties(editingGDB, hubGDB)

            try:

                aprx.save()
            except:
                logging.basicConfig(filename=logFile, level=logging.ERROR)
                logging.error(' Error with ArcGIS Pro project {}.'.format(m))
            del aprx

            logging.basicConfig(filename=logFile, level=logging.INFO)
            logging.info(' Data sources for {} were updated.'.format(m))

with open(csvFile, 'w') as g:
    writer = csv.writer(g)
    writer.writerow(['APRX File Path'])

message.Subject = "ArcGIS Pro Data Source Update - SUCCESS"
message.Html = "All ArcGIS Pro projects that had data pointing to the Editing geodatabase have been repointed to the Hub.<br><br>" \
               "Check the log (<a href='{}'>{}</a>) if you like.<br><br>" \
               "Or you can simply go on with your day.".format(logFile, logFile)
mailer = mailer.Mailer("mailhost.co.jeffco.us")
mailer.send(message)


finish = time.time()
duration = str(finish - start)

logging.basicConfig(filename=logFile, level=logging.INFO)
logging.info(' Sync was successful in {} seconds'.format(duration))
