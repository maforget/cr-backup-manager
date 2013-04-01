import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *
'''
Backup Manager for ComicRack
saves your ComicRack library file at each start of ComicRack

by docdoom

v 0.1.0
'''

from System.IO import File,  Directory, Path, FileInfo
import datetime

#@Name Backup Manager (Startup)
#@Hook Startup
#@Enabled true
#@Description Backup Manager (Startup)

def backupManager_Startup():
	now = datetime.datetime.now()
	myAppDataFolder = System.Environment.ExpandEnvironmentVariables('%appdata%') + '\\'
	myAppDataFolder = Path.Combine(myAppDataFolder,'cyo\\ComicRack') + '\\'
	myDBFile = Path.Combine(myAppDataFolder,'ComicDB.xml')
	currentDate = now.strftime("%Y-%m-%d_%H%M")

	FOLDER = FileInfo(__file__).DirectoryName + '\\'
	backupFolder = Path.Combine(FOLDER,'Backup') 

	if File.Exists(myDBFile):
		if not Directory.Exists(backupFolder):
			Directory.CreateDirectory(backupFolder)
		File.Copy(myDBFile,backupFolder + '\\ComicDB%s.xml' % currentDate, True)

