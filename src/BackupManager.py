
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

v 1.0.1

CHANGE - option for running the Backup Manager at Shutdown of CR

v 1.1 (by maforget)

CHANGE - Made compatible with ComicRack Community Edition, Alternate Config and Portable (will auto detect the data folder location).
	 (Unless you do a Full Backup, it will only save the current configuration DB & thumbnails)
CHANGE - Updated Zip Library to DotNetZip v1.16.0

v 1.2 (by maforget)

ADDED - Full Backup option on startup and shutdown

v 1.3 (by maforget)

CHANGED - Startup backup will now be done in the background and not freeze the program anymore

'''
myVersion = '1.3'
import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *
from System import Action
from System.Threading.Tasks import Task

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
		action = Action(lambda: bmUtil.do_the_backup(False, False))
		Task.Run(action)

#@Name Backup Manager - Full Backup (Startup)
#@Hook Startup
#@Enabled false
#@Description Backup Manager - Full Backup (Startup)

def backupManager_Full_Startup():
		setVersionInfo()
		bmUtil = backupManagerUtils()
		action = Action(lambda: bmUtil.do_the_backup(True, False))
		Task.Run(action)

#@Name Backup Manager (Shutdown)
#@Hook Shutdown
#@Enabled false
#@Description Backup Manager (Shutdown)

def backupManager_Shutdown(user_is_closing):
		print 'Shutting Down'
		bmUtil = backupManagerUtils()
		bmUtil.do_the_backup(False, False)
		return True		

#@Name Backup Manager - Full Backup (Shutdown)
#@Hook Shutdown
#@Enabled false
#@Description Backup Manager - Full Backup (Shutdown)

def backupManager_Full_Shutdown(user_is_closing):
		print 'Shutting Down'
		bmUtil = backupManagerUtils()
		bmUtil.do_the_backup(True, False)
		return True	
				
#@Name Backup Manager
#@Hook Library, Books
#@Image BackupMan.png
#@Description Backup Manager

def backupManager(books):
		setVersionInfo()
		form = MainForm()
		form.ShowDialog()
		form.Dispose()
		
					
					
					