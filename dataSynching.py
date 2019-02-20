import csv
import arcpy
import logging
import datetime
import os
import sys
import time
import mailer

# set up email object
message = mailer.Message()
# from email address
message.From = "jcos_gis@co.jefferson.co.us"
message.To = ["edelynko@co.jefferson.co.us", "cxwhite@co.jefferson.co.us", "cbouchar@co.jefferson.co.us", "rthayer@co.jefferson.co.us"]

# get beginning time to determine duration later
start = time.time()

# get date and time for logging purposes
todayDate = datetime.date.today()
d = str(todayDate).replace("-", "")
t = str(datetime.datetime.now()).split(" ")[1].split(".")[0]

# Set local variables
# Copy and Paste variables
hubDatabase = r'\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS\1_GIS_Hub\1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data.gdb'
editingDatabase = r'\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data___EDITING.gdb'
localLocation = r"C:\Jeffco_Open_Space_Managed_Data___EDITING.gdb"
backupLocation = r'\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Archive\Jeffco_Open_Space_Managed_Data___EDITING.gdb'
copyLocation = r'\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS\1_GIS_Hub\1_1_Org_Data\JCOS\Jeffco_Open_Space_Managed_Data___EDITING.gdb'
archiveRename = r'\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS_TEAM\1_GIS_Backups\1_1_Org_Data\Editing_1_1_Org_Data\JCOS\Archive\a{}_Jeffco_Open_Space_Managed_Data___EDITING.gdb'.format(d)

# log file
logFile = r"\\admin.co.jeffco.us\Files\Groups\Parks\OS\GIS_TEAM\3_Resources\3_1_GIS_Team\3_1_8_Tracking\Data_Sync_Log\{}.log".format(d)

# Function to find .lock files in Hub and Editing file geodatabases
def findLockFiles(srcDir):

    lockFileComputers = []
    computers = []

    # Set up os.walk
    for path, dirs, files in os.walk(srcDir):
        for fi in files:
            # Find files that end with .LOCK or .lock
            if fi.endswith(".LOCK") or fi.endswith(".lock"):
                # Append computer codes to empty list
                lockFileComputers.append(fi.split(".")[1])

    # Create a set (not a list, yet) of unique computers
    comps = set(lockFileComputers)

    # Create list of unique computers
    for computer in comps:
        computers.append(computer)
    return computers


# From function return value, determine the computers with locks
hubComputersWithLocks = findLockFiles(hubDatabase)
editingComputersWithLocks = findLockFiles(editingDatabase)

# if/else statement determining if the 'computer' lists were populated and what to do
if len(findLockFiles(hubDatabase)) > 0 or len(findLockFiles(editingDatabase)) > 0:
    for h in hubComputersWithLocks:
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(' Computer -- {} -- had a schema lock in the Hub Database at {}'.format(h, t))
    for e in editingComputersWithLocks:
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(' Computer -- {} -- had a schema lock in the Editing Database at {}'.format(e, t))

    message.Subject = "Data Syncing - FAILURE"
    message.Html = "The automatic syncing script failed to run due to a lock in either the Hub or editing file geodatabase.\nPlease check the log:\n<a href='{}'>{}</a>".format(logFile, logFile)
    mailer = mailer.Mailer("mailhost.co.jeffco.us")
    mailer.send(message)
    sys.exit()

else:
    # CODE FOR SYNCING DATA

    # Execute Copy and Paste (Backup)
    try:
        arcpy.Rename_management(backupLocation, archiveRename)

    except:
        print(arcpy.GetMessages())
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(" Unable to rename database in Archive folder. Why? It's a mystery")
        logging.error(arcpy.GetMessages())

        message.Subject = "Data Syncing - FAILURE"
        message.Html = "The automatic syncing script failed." \
                       "Please check the log:" \
                       "<a href='{}'>{}</a>".format(logFile, logFile)
        mailer = mailer.Mailer("mailhost.co.jeffco.us")
        mailer.send(message)
        sys.exit()

    # Execute Delete
    try:
        arcpy.Delete_management(hubDatabase)

    except:
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(' Unable to delete Hub database')

        message.Subject = "Data Syncing - FAILURE"
        message.Html = "The automatic syncing script was unable to delete the Hub database. It is unknown why. Please manually run the script again."
        mailer = mailer.Mailer("mailhost.co.jeffco.us")
        mailer.send(message)
        sys.exit()

    # Execute Rename
    try:
        arcpy.Rename_management(copyLocation, hubDatabase)
    except:
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(' Unable to rename Editing to Hub')

        message.Subject = "Data Syncing - FAILURE"
        message.Html = "The automatic syncing script was unable to rename the Editing database to the Hub. It is unknown why. Please manually run the script again."
        mailer = mailer.Mailer("mailhost.co.jeffco.us")
        mailer.send(message)

        sys.exit()

    # Delete local file geodatabase
    try:
        arcpy.Delete_management(localLocation)

    except:
        logging.basicConfig(filename=logFile, level=logging.ERROR)
        logging.error(' Unable to delete Hub database')

        message.Subject = "Data Syncing - FAILURE"
        message.Html = "The automatic syncing script was unable to delete the temporary database stored locally. It is unknown why. Please manually run the script again."
        mailer = mailer.Mailer("mailhost.co.jeffco.us")
        mailer.send(message)
        sys.exit()

finish = time.time()
duration = str(finish - start)

logging.basicConfig(filename=logFile, level=logging.INFO)
logging.info(' Sync was successful in {} seconds'.format(duration))

message.Subject = "Data Syncing and MXD Data Source Update - SUCCESS"

message.Html = "The automatic syncing script ran without error.<br><br>" \
               "Log file: (<a href='{}'>{}</a>)<br><br>".format(logFile, logFile)
mailer = mailer.Mailer("mailhost.co.jeffco.us")
mailer.send(message)
