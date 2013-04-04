'''
Backup Manager for ComicRack
bmUtils.py - utility classes for the Backup Manager

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

'''

import clr
import System.Windows.Forms
from System.Windows.Forms import *
import datetime
import System.IO
from System.IO import Path, FileInfo, File, Directory

clr.AddReference('Ionic.Zip')
from Ionic.Zip import *

FOLDER = FileInfo(__file__).DirectoryName + '\\'
INIFILE = Path.Combine(FOLDER, 'backupMan.ini')
ICONLARGE = Path.Combine(FOLDER, 'backupManLarge.png')
FILENUMBERWARNING = 100		# threshold of backup file count


class backupManagerUtils:
	def __init__(self):

		pass
	
	def setBackupFolder(self):
		ini = iniFile()
		dialog = FolderBrowserDialog()
		dialog.Description = 'The Backup Manager for ComicRack\n\nPlease select where to store your backups'
		root = ini.getValue(INIFILE,'backupFolder')
		version = ini.getValue(INIFILE, 'Version')
		if str.Trim(root) <> '':
			dialog.SelectedPath = root
		else:
			dialog.RootFolder = System.Environment.SpecialFolder.Desktop
		if dialog.ShowDialog() == DialogResult.OK:
			ini.writeIni(INIFILE,'backupFolder',dialog.SelectedPath)
			return True
		else:
			return False
			
	def do_the_backup(self, FULLBACKUP = False, SHOWRESULT = False):
		ini = iniFile()
		version = ini.getValue(INIFILE, 'Version')
		msgBoxTitle = 'Backup Manager for ComicRack %s' % version
		backupFolder = ''
		if not File.Exists(INIFILE):
			self.setBackupFolder()
		else:
			backupFolder = ini.getValue(INIFILE,'backupFolder')
		if str.Trim(backupFolder) == '':
			return self.setBackupFolder()
		elif not Directory.Exists(backupFolder):
			MessageBox.Show('The path for your backup is not valid. Please configure!', msgBoxTitle)
			return self.setBackupFolder()
		else:
			if Directory.GetFiles(backupFolder,'ComicDB*.zip').Length > FILENUMBERWARNING:
				MessageBox.Show('There are a lot of backup files in your backupfolder.\nYou should consider a clean-up', msgBoxTitle)
			now = datetime.datetime.now()
			myAppDataFolder = System.Environment.ExpandEnvironmentVariables('%appdata%') + '\\'
			myAppDataFolder = Path.Combine(myAppDataFolder,'cyo\\ComicRack') + '\\'
			myDBFile = Path.Combine(myAppDataFolder,'ComicDB.xml')
			myConfigXML = Path.Combine(myAppDataFolder,'config.xml')
			myDate = now
			currentDate = myDate.strftime("%Y-%m-%d_%H%M%S")
	
			zipfile = ZipFile()
			if not File.Exists(myDBFile):
				MessageBox.Show('I could not find your library file. Please post this error.', msgBoxTitle)	
			else:
				if not Directory.Exists(backupFolder):
					Directory.CreateDirectory(backupFolder)
				
				if FULLBACKUP == True:
					myBackup = backupFolder + '\\ComicDB Full Backup %s.zip' % currentDate
					zipfile.AddDirectory(myAppDataFolder)
				else:
					myBackup = backupFolder + '\\ComicDB Backup %s.zip' % currentDate
					zipfile.AddFile(myDBFile,'')
				zipfile.Save(myBackup)

				if SHOWRESULT == True:
					if File.Exists(myBackup) and SHOWRESULT == True:
						MessageBox.Show('Backup saved as \n%s' % myBackup, msgBoxTitle)
						ini.writeIni(INIFILE,'LastBackupTime', myDate.strftime("%Y-%m-%d %H:%M:%S"))
					else:
						MessageBox.Show('No backup file was saved. Something unexpected must have happened ...', msgBoxTitle)
		return True

class iniFile:
	def __init__(self):
		pass
	
	def writeIni(self, theFile, myKey, myVal):
		'''
		writes the key myKey and value myVal to the ini-file
		'''

		if File.Exists(theFile):
			linefound = False
			newConfig = []
			myLines = File.ReadAllLines(theFile)
			for line in myLines:
				s = str.split(line,'=')
				if str.lower(str.Trim(s[0])) == str.lower(myKey):
					line = '%s = %s' % (myKey, myVal)
					linefound = True
				newConfig.append(line)
			if linefound == False:
				newConfig.append('%s = %s' % (myKey, myVal))
			File.WriteAllLines(theFile,newConfig)
		else:
			File.AppendAllText(theFile,'%s = %s%s' % (myKey, myVal, System.Environment.NewLine))
		return
	
	
	def getValue(self, theFile, myKey):
		'''
		retrieves the value of myKey in Ini-file theFile
		'''
		if File.Exists(theFile):
			myLines = File.ReadAllLines(theFile)
			for line in myLines:
				s = str.split(line,'=')
				if str.Trim(s[0]) == myKey:
					return str.Trim(s[1])
		return ''
	

	
