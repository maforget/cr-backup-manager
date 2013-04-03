
'''
Backup Manager for ComicRack
saves your ComicRack library file at each start of ComicRack

by docdoom

Ionic zip library used with permission from http://dotnetzip.codeplex.com
Icons and images used with permission from http://jonasraskdesign.com

v 0.1.2

CHANGE - backups are stored as ZIP files so they can easily be restored from within CR
CHANGE - threshold set to comicdb*.zip instead of *.xml
CHANGE - result MessageBox redesigned
CHANGE - dialogs display version number
CHANGE - root folder for folder browser is now DESKTOP instead of PERSONAL
CHANGE - form and methods moved to own modules
CHANGE - full backup of %appdata%\cyo\comicrack is supported
CHANGE - icons added

'''

import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

import System.IO
from System.IO import File,  Directory, Path, FileInfo

from MainForm import MainForm

import bmUtils
from bmUtils import *


#@Name Backup Manager (Startup)
#@Hook Startup
#@Enabled true
#@Description Backup Manager (Startup)

def backupManager_Startup():
	bmUtil = backupManagerUtils()
	bmUtil.do_the_backup(False, False)


#@Name Backup Manager
#@Hook Library, Books
#@Image BackupMan.png
#@Description Backup Manager

def backupManager(books):

	form = MainForm()
	form.ShowDialog()
	form.Dispose()
	
	return


	