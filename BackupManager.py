
'''
Backup Manager for ComicRack
saves your ComicRack library file at each start of ComicRack

by docdoom

The CR Data Manager plugin is licensed under the Apache 2.0 software
license, available at: http://www.apache.org/licenses/LICENSE-2.0.html

Ionic zip library used with permission from http://dotnetzip.codeplex.com
Icons and images used with permission from http://jonasraskdesign.com

v 0.1.2

CHANGE - backups are stored as ZIP files so they can easily be restored from within CR
CHANGE - threshold set to comicdb*.zip instead of *.xml
CHANGE - result MessageBox redesigned
CHANGE - version info added to dialogs
CHANGE - root folder for folder browser is now DESKTOP instead of PERSONAL
CHANGE - form and methods moved to own modules
CHANGE - full backup of %appdata%\cyo\comicrack is supported
CHANGE - icons added
CHANGE - license info added
CHANGE - version info written to and read from ini file (issue 10)
FIXED - main dialog is closed if ini exists but no valid backupFolder key is found (issue 9)

'''
myVersion = '0.1.2 r22'
import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

import System.IO
from System.IO import File,  Directory, Path, FileInfo

print 'step 1'
import MainForm
from MainForm import MainForm
print 'step 2'
import bmUtils
from bmUtils import *

def setVersionInfo():
		ini = bmUtils.iniFile()
		ini.writeIni(INIFILE, 'Version', myVersion)
		
#@Name Backup Manager (Startup)
#@Hook Startup
#@Enabled true
#@Description Backup Manager (Startup)

def backupManager_Startup():
		setVersionInfo()
		bmUtil = backupManagerUtils()
		bmUtil.do_the_backup(False, False)
		
				
#@Name Backup Manager
#@Hook Library, Books
#@Image BackupMan.png
#@Description Backup Manager

def backupManager(books):
		setVersionInfo()
		form = MainForm()
		form.ShowDialog()
		form.Dispose()
		
		return
					
					
					