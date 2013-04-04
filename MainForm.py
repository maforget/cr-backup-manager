import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

import bmUtils
from bmUtils import *


class MainForm(Form):
	def __init__(self):

		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._buttonRun = System.Windows.Forms.Button()
		self._buttonConfigure = System.Windows.Forms.Button()
		self._buttonCancel = System.Windows.Forms.Button()
		self._checkBoxFullBackup = System.Windows.Forms.CheckBox()
		self._toolTip1 = System.Windows.Forms.ToolTip(self._components)
		self._pictureBox1 = System.Windows.Forms.PictureBox()
		self._pictureBox1.BeginInit()
		self.SuspendLayout()
		# 
		# buttonRun
		# 
		self._buttonRun.Location = System.Drawing.Point(12, 34)
		self._buttonRun.Name = "buttonRun"
		self._buttonRun.Size = System.Drawing.Size(75, 23)
		self._buttonRun.TabIndex = 1
		self._buttonRun.Text = "Backup"
		self._toolTip1.SetToolTip(self._buttonRun, """Backups ComicDB.xml only
(unless \"full backup\" is checked)""")
		self._buttonRun.UseVisualStyleBackColor = True
		self._buttonRun.Click += self.ButtonRunClick
		# 
		# buttonConfigure
		# 
		self._buttonConfigure.Location = System.Drawing.Point(115, 34)
		self._buttonConfigure.Name = "buttonConfigure"
		self._buttonConfigure.Size = System.Drawing.Size(75, 23)
		self._buttonConfigure.TabIndex = 2
		self._buttonConfigure.Text = "Configure"
		self._toolTip1.SetToolTip(self._buttonConfigure, """Select the folder where your backups
will be stored""")
		self._buttonConfigure.UseVisualStyleBackColor = True
		self._buttonConfigure.Click += self.ButtonConfigureClick
		# 
		# buttonCancel
		# 
		self._buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
		self._buttonCancel.Location = System.Drawing.Point(222, 34)
		self._buttonCancel.Name = "buttonCancel"
		self._buttonCancel.Size = System.Drawing.Size(75, 23)
		self._buttonCancel.TabIndex = 3
		self._buttonCancel.Text = "Cancel"
		self._toolTip1.SetToolTip(self._buttonCancel, "leave this dialog")
		self._buttonCancel.UseVisualStyleBackColor = True
		# 
		# checkBoxFullBackup
		# 
		self._checkBoxFullBackup.Location = System.Drawing.Point(12, 63)
		self._checkBoxFullBackup.Name = "checkBoxFullBackup"
		self._checkBoxFullBackup.Size = System.Drawing.Size(104, 24)
		self._checkBoxFullBackup.TabIndex = 4
		self._checkBoxFullBackup.Text = "full backup"
		self._toolTip1.SetToolTip(self._checkBoxFullBackup, """if checked this backup will contain the 
complete folder %appdata%\\roaming\\cyo\\comicrack
including all subfolders""")
		self._checkBoxFullBackup.UseVisualStyleBackColor = True
		# 
		# pictureBox1
		# 
		self._pictureBox1.Location = System.Drawing.Point(122, -10)
		self._pictureBox1.Name = "pictureBox1"
		self._pictureBox1.Size = System.Drawing.Size(128, 128)
		self._pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize
		self._pictureBox1.TabIndex = 5
		self._pictureBox1.TabStop = False
		# 
		# MainForm
		# 
		self.CancelButton = self._buttonCancel
		self.ClientSize = System.Drawing.Size(312, 109)
		self.Controls.Add(self._checkBoxFullBackup)
		self.Controls.Add(self._buttonCancel)
		self.Controls.Add(self._buttonConfigure)
		self.Controls.Add(self._buttonRun)
		self.Controls.Add(self._pictureBox1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "MainForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Backup Manager for ComicRack %s"
		self.Load += self.MainFormLoad
		self.CursorChanged += self.MainFormCursorChanged
		self._pictureBox1.EndInit()
		self.ResumeLayout(False)
		self.PerformLayout()

	def ButtonConfigureClick(self, sender, e):
		bmUtil = backupManagerUtils()
		bmUtil.setBackupFolder()

	def ButtonRunClick(self, sender, e):
		bmUtil = backupManagerUtils()
		
		fullBackup = self._checkBoxFullBackup.Checked == True
		showResults = True
		self.Cursor = Cursors.WaitCursor
		if bmUtil.do_the_backup(fullBackup, showResults) == True:
			print 'should close here'
			self._buttonRun.DialogResult = System.Windows.Forms.DialogResult.OK
			self.Dispose()
		self.Cursor = Cursors.Default


	def MainFormLoad(self, sender, e):
		ini = bmUtils.iniFile()
		version = ini.getValue(INIFILE, 'Version')
		self.Text = 'Backup Manager for ComicRack %s' % version
		self._pictureBox1.Image = System.Drawing.Image.FromFile(ICONLARGE)

	def MainFormCursorChanged(self, sender, e):
		pass