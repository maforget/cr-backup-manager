
'''
Backup Manager for ComicRack
saves your ComicRack library file at each start of ComicRack

by docdoom

Ionic zip library used with permission from http://dotnetzip.codeplex.com

v 0.1.2

CHANGE - backups are stored as ZIP files so they can easily be restored from within CR

'''

import clr
import System
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import *
from System.Drawing import *

import System.IO
from System.IO import File,  Directory, Path, FileInfo
import datetime

clr.AddReference('Ionic.Zip')
from Ionic.Zip import *

FOLDER = FileInfo(__file__).DirectoryName + '\\'
INIFILE = Path.Combine(FOLDER, 'backupMan.ini')
SHOWRESULT = False			# display result of backup
FILENUMBERWARNING = 500		# threshold of backup file count

def createZip(theZip,theFile):
	'''
	creates a ZIP file theZip and stores theFile in it
	'''
	print 'theZip: %s' % theZip
	print 'theFile: %s' % theFile
	
	zipfile = ZipFile()
	zipfile.AddFile(theFile,'')
	zipfile.Save(theZip)

	return
	

def writeIni(theFile, myKey, myVal):
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

def getValue(theFile, myKey):
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

def setBackupFolder():
		dialog = FolderBrowserDialog()
		dialog.Description = 'The Backup Manager for ComicRack\n\nPlease select where to store your backups'
		root = getValue(INIFILE,'backupFolder')
		if str.Trim(root) <> '':
			dialog.SelectedPath = root
		else:
			dialog.RootFolder = System.Environment.SpecialFolder.Personal
		if dialog.ShowDialog() == DialogResult.OK:
			writeIni(INIFILE,'backupFolder',dialog.SelectedPath)

		form = bmMainForm()
		form.ShowDialog()
		form.Dispose()

class bmMainForm(Form):
	def __init__(self):
		self.buttonRun = Button()
		self.buttonConfig = Button()
		self.buttonCancel = Button()
		self.Label1 = Label()
		self.SuspendLayout()
		
		# buttonRun
		
		self.buttonRun.Location = Point(28, 57)
		self.buttonRun.Name = "buttonRun"
		self.buttonRun.Size = Size(75, 23)
		self.buttonRun.TabIndex = 0
		self.buttonRun.Text = "Run"
		self.buttonRun.UseVisualStyleBackColor = True
		self.buttonRun.Click += self.run
		self.buttonRun.DialogResult = DialogResult.OK
		
		#buttonConfig
		
		self.buttonConfig.Location = Point(129, 57)
		self.buttonConfig.Name = "buttonConfig"
		self.buttonConfig.Size = Size(75, 23)
		self.buttonConfig.TabIndex = 1
		self.buttonConfig.Text = "Configure"
		self.buttonConfig.UseVisualStyleBackColor = True
		self.buttonConfig.Click += self.config
		
		# buttonCancel
		
		self.buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self.buttonCancel.Location = Point(224, 57)
		self.buttonCancel.Name = "buttonCancel"
		self.buttonCancel.Size = Size(75, 23)
		self.buttonCancel.TabIndex = 2
		self.buttonCancel.Text = "Cancel"
		self.buttonCancel.UseVisualStyleBackColor = True
		
		# Label1
		
		self.Label1.AutoSize = True
		self.Label1.Location = Point(25, 20)
		self.Label1.Name = "Label1"
		self.Label1.Size = Size(167, 13)
		self.Label1.TabIndex = 3
		self.Label1.Text = "Welcome to the Backup Manager"
		
		# Form1
		
		self.CancelButton = self.buttonCancel
		self.ClientSize = Size(339, 105)
		self.Controls.Add(self.Label1)
		self.Controls.Add(self.buttonCancel)
		self.Controls.Add(self.buttonConfig)
		self.Controls.Add(self.buttonRun)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Text = "Backup Manager for ComicRack"
		self.ResumeLayout(False)
		self.PerformLayout()

	def config(self, sender, event):
		setBackupFolder()

	def run(self, sender, event):
		self.Cursor = Cursors.WaitCursor
		backupManager_Startup()
		self.Cursor = Cursors.Default
		self.buttonRun.DialogResult = DialogResult.OK

#@Name Backup Manager (Startup)
#@Hook Startup
#@Enabled true
#@Description Backup Manager (Startup)

def backupManager_Startup():
	backupFolder = ''
	if not File.Exists(INIFILE):
		setBackupFolder()
	else:
		backupFolder = getValue(INIFILE,'backupFolder')

	if str.Trim(backupFolder) <> '':
		if Directory.GetFiles(backupFolder,'*.xml').Length > FILENUMBERWARNING:
			MessageBox.Show('There are a lot of backup files in your backupfolder.\nYou should consider a clean-up')
		now = datetime.datetime.now()
		myAppDataFolder = System.Environment.ExpandEnvironmentVariables('%appdata%') + '\\'
		myAppDataFolder = Path.Combine(myAppDataFolder,'cyo\\ComicRack') + '\\'
		myDBFile = Path.Combine(myAppDataFolder,'ComicDB.xml')
		currentDate = now.strftime("%Y-%m-%d_%H%M%S")

		if File.Exists(myDBFile):
			if not Directory.Exists(backupFolder):
				Directory.CreateDirectory(backupFolder)

			myBackup = backupFolder + '\\ComicDB Backup %s.zip' % currentDate
			createZip(myBackup, myDBFile)
			
			if SHOWRESULT == True:
				if File.Exists(myBackup) and SHOWRESULT == True:
					MessageBox.Show('Backup saved as %s' % myBackup)
				else:
					MessageBox.Show('No backup file was saved.')


#@Name Backup Manager
#@Hook Library, Books
#@Image Backup-Green-Button-icon.png
#@Description Backup Manager

def backupManager(books):

	global SHOWRESULT
	SHOWRESULT = True
	form = bmMainForm()
	form.ShowDialog()
	form.Dispose()

	