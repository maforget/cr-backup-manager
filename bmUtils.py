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
FILENUMBERWARNING = 500		# threshold of backup file count

VERSION = '0.1.2 r20'
		
class backupManagerUtils:
	def __init__(self):
		pass
	
	def setBackupFolder(self):
		ini = iniFile()
		dialog = FolderBrowserDialog()
		dialog.Description = 'The Backup Manager for ComicRack\n\nPlease select where to store your backups'
		root = ini.getValue(INIFILE,'backupFolder')
		if str.Trim(root) <> '':
			dialog.SelectedPath = root
		else:
			dialog.RootFolder = System.Environment.SpecialFolder.Desktop
		if dialog.ShowDialog() == DialogResult.OK:
			ini.writeIni(INIFILE,'backupFolder',dialog.SelectedPath)
			
	def do_the_backup(self, FULLBACKUP = False, SHOWRESULT = False):
		ini = iniFile()
		print 'do_the_backup()'
		backupFolder = ''
		if not File.Exists(INIFILE):
			setBackupFolder()
		else:
			backupFolder = ini.getValue(INIFILE,'backupFolder')
		if str.Trim(backupFolder) <> '':
			if Directory.GetFiles(backupFolder,'ComicDB*.zip').Length > FILENUMBERWARNING:
				MessageBox.Show('There are a lot of backup files in your backupfolder.\nYou should consider a clean-up')
			now = datetime.datetime.now()
			myAppDataFolder = System.Environment.ExpandEnvironmentVariables('%appdata%') + '\\'
			myAppDataFolder = Path.Combine(myAppDataFolder,'cyo\\ComicRack') + '\\'
			myDBFile = Path.Combine(myAppDataFolder,'ComicDB.xml')
			myConfigXML = Path.Combine(myAppDataFolder,'config.xml')
			currentDate = now.strftime("%Y-%m-%d_%H%M%S")
	
			zipfile = ZipFile()
			if not File.Exists(myDBFile):
				MessageBox.Show('I could not find your library file. Please post this error.')	
			else:
				if not Directory.Exists(backupFolder):
					Directory.CreateDirectory(backupFolder)
				
				if FULLBACKUP == True:
					myBackup = backupFolder + '\\ComicDB Full Backup %s.zip' % currentDate
					print 'backup starting'
					zipfile.AddDirectory(myAppDataFolder)
					zipfile.Save(myBackup)
				else:
					myBackup = backupFolder + '\\ComicDB Backup %s.zip' % currentDate
					zipfile.AddFile(myDBFile,'')
#					if ADDCONFIGXML == True:
#						zipfile.AddFile(myConfigXML,'')
					zipfile.Save(myBackup)

				print 'showResult: %s' % SHOWRESULT
				if SHOWRESULT == True:
					if File.Exists(myBackup) and SHOWRESULT == True:
						MessageBox.Show('Backup saved as \n%s' % myBackup, 'Backup Manager for ComicRack %s' % VERSION)
					else:
						MessageBox.Show('No backup file was saved. Something unexpected must have happened ...')
		return

class iniFile:
	def __init__(self):
		pass
	
	def writeIni(self, theFile, myKey, myVal):
		'''
		writes the key myKey and value myVal to the ini-file
		'''
		if File.Exists(theFile):
			newConfig = []
			myLines = File.ReadAllLines(theFile)
			for line in myLines:
				s = str.split(line,'=')
				if str.Trim(s[0]) == myKey:
					line = '%s = %s' % (myKey, myVal)
				newConfig.append(line)
			File.WriteAllLines(theFile,newConfig)
		else:
			File.AppendAllText(theFile,'%s = %s%s' % (myKey, myVal, System.Environment.NewLine))

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
	
