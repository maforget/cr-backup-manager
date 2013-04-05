
'''
Backup Manager for ComicRack
BackupManager.py - contains only the entrance hooks for ComicRack

Copyright 2013 docdoom

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Ionic zip library used with permission from http://dotnetzip.codeplex.com
Icons and images used with permission from http://jonasraskdesign.com

v 1.0

CHANGE - backups are stored as ZIP files so they can easily be restored from within CR
CHANGE - threshold set to comicdb*.zip instead of *.xml
CHANGE - result MessageBox redesigned
CHANGE - version info added to dialogs
CHANGE - root folder for folder browser is now DESKTOP instead of PERSONAL
CHANGE - form and methods moved to own modules
CHANGE - full backup of %appdata%\cyo\comicrack is supported
CHANGE - icons added (issue 4)
CHANGE - license info added
CHANGE - version info written to and read from ini file (issue 10)
FIXED - main dialog is closed if ini exists but no valid backupFolder key is found (issue 9)
FIXED - invalid path raises DirectoryNotFoundException (issue 11)
FIXED - Most of the MessageBoxes have no title and version info (issue 12)
CHANGE - Last backup time added to ini file
FIXED - Values in ini file are not overwritten but added to end of ini file (issue 13)
FIXED - Config dialog has to be canceled even after successfully running the script (issue 6)
FIXED - package.ini should include reference to Backup Manager icon
FIXED - both normal and full backups should include custom thumbnail folders

'''
myVersion = '1.0 r29'
import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

import System.IO
from System.IO import File,  Directory, Path, FileInfo

import MainForm
from MainForm import MainForm
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
		
					
					
					