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
		self._label1 = System.Windows.Forms.Label()
		self._buttonRun = System.Windows.Forms.Button()
		self._buttonConfigure = System.Windows.Forms.Button()
		self._buttonCancel = System.Windows.Forms.Button()
		self._checkBoxFullBackup = System.Windows.Forms.CheckBox()
		self._toolTip1 = System.Windows.Forms.ToolTip(self._components)
		self.SuspendLayout()
		# 
		# label1
		# 
		self._label1.Location = System.Drawing.Point(13, 13)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(248, 23)
		self._label1.TabIndex = 0
		self._label1.Text = "Welcome to the Backup Manager"
		# 
		# buttonRun
		# 
		self._buttonRun.DialogResult = System.Windows.Forms.DialogResult.OK
		self._buttonRun.Location = System.Drawing.Point(13, 50)
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
		self._buttonConfigure.Location = System.Drawing.Point(120, 50)
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
		self._buttonCancel.Location = System.Drawing.Point(224, 49)
		self._buttonCancel.Name = "buttonCancel"
		self._buttonCancel.Size = System.Drawing.Size(75, 23)
		self._buttonCancel.TabIndex = 3
		self._buttonCancel.Text = "Cancel"
		self._toolTip1.SetToolTip(self._buttonCancel, "leave this dialog")
		self._buttonCancel.UseVisualStyleBackColor = True
		# 
		# checkBoxFullBackup
		# 
		self._checkBoxFullBackup.Location = System.Drawing.Point(12, 79)
		self._checkBoxFullBackup.Name = "checkBoxFullBackup"
		self._checkBoxFullBackup.Size = System.Drawing.Size(104, 24)
		self._checkBoxFullBackup.TabIndex = 4
		self._checkBoxFullBackup.Text = "full backup"
		self._toolTip1.SetToolTip(self._checkBoxFullBackup, """if checked this backup will contain the 
complete folder %appdata%\\roaming\\cyo\\comicrack
including all subfolders""")
		self._checkBoxFullBackup.UseVisualStyleBackColor = True
		# 
		# MainForm
		# 
		self.CancelButton = self._buttonCancel
		self.ClientSize = System.Drawing.Size(324, 109)
		self.Controls.Add(self._checkBoxFullBackup)
		self.Controls.Add(self._buttonCancel)
		self.Controls.Add(self._buttonConfigure)
		self.Controls.Add(self._buttonRun)
		self.Controls.Add(self._label1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
		self.MaximizeBox = False
		self.MinimizeBox = False
		self.Name = "MainForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent
		self.Text = "Backup Manager for ComicRack %s"
		self.Load += self.MainFormLoad
		self.CursorChanged += self.MainFormCursorChanged
		self.ResumeLayout(False)

	def ButtonConfigureClick(self, sender, e):
		bmUtil = backupManagerUtils()
		bmUtil.setBackupFolder()

	def ButtonRunClick(self, sender, e):
		bmUtil = backupManagerUtils()
		
		fullBackup = self._checkBoxFullBackup.Checked == True
		showResults = True
		self.Cursor = Cursors.WaitCursor
		bmUtil.do_the_backup(fullBackup, showResults)
		self.Cursor = Cursors.Default


	def MainFormLoad(self, sender, e):
		self.Text = 'Backup Manager for ComicRack %s' % VERSION

	def MainFormCursorChanged(self, sender, e):
		pass