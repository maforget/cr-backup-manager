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
from System.IO import Path, FileInfo, File, Directory, DirectoryInfo, SearchOption

clr.AddReference('DotNetZip')
from Ionic.Zip import *

FOLDER = FileInfo(__file__).DirectoryName + '\\'
INIFILE = Path.Combine(FOLDER, 'backupMan.ini')
ICONLARGE = Path.Combine(FOLDER, 'backupManLarge.png')
FILENUMBERWARNING = 100		# threshold of backup file count

class AlternateConfig:

    ConfigName = ''
    ConfigPath = ''

    def __init__(self):
        pass
        
    def setValue(self, configName, configPath):
        self.ConfigName = configName
        self.ConfigPath = configPath    
        
    def isEmpty(self):
        if self.ConfigName and self.ConfigPath:
            return False
        
        return True

class Folder:

    FolderName = ''
    FullPath = ''
    Portable = False
    Config = AlternateConfig()

    def __init__(self, folderName, fullPath, config, portable = False):
        self.FolderName = folderName
        self.FullPath = fullPath
        self.Portable = portable
        self.Config = config

    @staticmethod
    def FindDataFolder(startingDir, config = AlternateConfig()):           
        upDir = DirectoryInfo(startingDir).Parent

        if upDir:

            if upDir.Name == 'Configurations':
                di = DirectoryInfo(startingDir)
                config.setValue(di.Name, di.FullName)
            
            #Path contains either the 'ComicRack' (for either ComicRackCE or the Original) or 'Data' folder (for Portable)
            if upDir.Name == 'Data':
                return Folder(upDir.Name, upDir.FullName, config, True)
            
            if 'ComicRack' in upDir.Name:
                return Folder(upDir.Name, upDir.FullName, config)
            
            result = Folder.FindDataFolder(upDir.FullName, config)
            return result

        return None
    

class backupManagerUtils:
    def __init__(self):
        pass
    
    def setBackupFolder(self):
        ini = iniFile()
        dialog = FolderBrowserDialog()
        dialog.Description = 'The Backup Manager for ComicRack\n\nPlease select where to store your backups'
        root = ini.getValue(INIFILE,'backupFolder')
        version = ini.getValue(INIFILE, 'Version')
        if str.Trim(root) != '':
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
                MessageBox.Show('There are a lot of backup files in your backup folder.\nYou should consider a clean-up', msgBoxTitle)

            myFolder = Folder.FindDataFolder(FOLDER)               
            if myFolder:
                isConfig = False if myFolder.Config.isEmpty() else True
                configName = myFolder.Config.ConfigName if isConfig else ''
                configPath = myFolder.Config.ConfigPath if isConfig else ''
            
                prefix = 'cYo\\' + myFolder.FolderName + '\\' #Only used with a non portable install
                prefixConfig = prefix + 'Configurations\\' + configName + '\\' if isConfig and FULLBACKUP == False else prefix #Build Config path when using an alternateConfig
                localPrefix = 'Local\\' + prefix #Only used with a non portable install with a FULL BACKUP
                roamingPrefix = 'Roaming\\' + prefix #Only used with a non portable install with a FULL BACKUP
                thumbnailPath = 'Cache\\CustomThumbnails'

                myAppDataFolder = configPath if isConfig and FULLBACKUP == False else myFolder.FullPath #Gets the normal root of the data folder unless we are using a config and not doing a FULL BACKUP 
                localAppPath = Path.Combine(System.Environment.ExpandEnvironmentVariables('%LOCALAPPDATA%'), prefixConfig) #Handles configs because of previous check on prefix
                
                myDBFile = Path.Combine(myAppDataFolder,'ComicDB.xml')
                myConfigXML = Path.Combine(myAppDataFolder,'Config.xml')
                myDate = datetime.datetime.now()
                currentDate = myDate.strftime("%Y-%m-%d_%H%M%S")

                portable = '(Portable) ' if myFolder.Portable else ''
                full = 'Full ' if FULLBACKUP else ''
                config = '(Config = ' + configName + ') ' if isConfig and FULLBACKUP == False else '' 
                myBackup = backupFolder + '\\ComicDB %s%s%sBackup %s.zip' % (full, portable, config, currentDate)
    
                zipfile = ZipFile()
                if not File.Exists(myDBFile):
                    MessageBox.Show('I could not find your library file. Please post this error.', msgBoxTitle)	
                else:
                    if not Directory.Exists(backupFolder):
                        Directory.CreateDirectory(backupFolder)
                    
                    if FULLBACKUP == True:
                        if myFolder.Portable:
                            backupManagerUtils.add_files_to_zip(zipfile, myAppDataFolder, 'Cache', thumbnailPath) #Using this method here, because I don't want to add the other Cache files
                        else:
                            backupManagerUtils.add_files_to_zip(zipfile, myAppDataFolder, prefix = roamingPrefix)
                            backupManagerUtils.add_files_to_zip(zipfile, localAppPath, 'Cache', thumbnailPath, prefix = localPrefix)
                    else:
                        if myFolder.Portable:
                            zipfile.AddFile(myDBFile,'')
                            zipfile.AddDirectory(Path.Combine(myAppDataFolder, thumbnailPath), 'Thumbnails')
                        else:
                            zipfile.AddFile(myDBFile, '')
                            zipfile.AddDirectory(Path.Combine(localAppPath, thumbnailPath), 'Thumbnails')
                    
                    zipfile.Save(myBackup)

                    if SHOWRESULT == True:
                        if File.Exists(myBackup) and SHOWRESULT == True:
                            MessageBox.Show('Backup saved as \n%s' % myBackup, msgBoxTitle)
                            ini.writeIni(INIFILE,'LastBackupTime', myDate.strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            MessageBox.Show('No backup file was saved. Something unexpected must have happened ...', msgBoxTitle)
        return True
    
    @staticmethod
    def add_files_to_zip(zip_file, source_folder, excluded_folder = '', allowed_subfolder = '', prefix = '', only_include_from_allowed_subfolder = False):
        di = DirectoryInfo(source_folder)
        files = di.EnumerateFiles('*', SearchOption.AllDirectories)
        # What about empty folders? Should we add them also?
        
        for fi in files:
            # if the files contains the excluded folder but not the allowed subfolder, then continue to the next file
            if excluded_folder and allowed_subfolder and excluded_folder in fi.DirectoryName and not (allowed_subfolder in fi.DirectoryName):
                continue
            
            # if the only_include_from_allowed_subfolder is True and the files aren't in the subfolder, then go to the next file
            if only_include_from_allowed_subfolder and allowed_subfolder and not (allowed_subfolder in fi.DirectoryName):
                continue

            # Add every other files that wasn't excluded
            entry_name = backupManagerUtils.get_relative_path(fi.DirectoryName, source_folder)
            zip_file.AddFile(fi.FullName, prefix + entry_name)

    @staticmethod
    def get_relative_path(destination_folder, base_folder):
        base_folder = base_folder.TrimEnd('\\')
        destination_folder = destination_folder.TrimEnd('\\')

        return destination_folder[len(base_folder) + 1:]

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
    

    
