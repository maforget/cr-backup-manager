### You should consider using [ComicRack Community Edition](https://github.com/maforget/ComicRackCE). And if you can please contribute to the project.

# Backup Manager for ComicRack

docdoom (updated by maforget) Proudly Presents the Backup Manager for ComicRack

This little plugin automates the process of saving the ComicRack library file. See the manual here for further information.
Major changes in version 1.1 (by maforget)

* CHANGE - Made compatible with ComicRack Community Edition, Alternate Config and Portable (will auto detect the data folder location).
    * Unless you do a Full Backup, it will only save the current configuration DB & thumbnails.
* CHANGE - Updated Zip Library to DotNetZip v1.16.0

Backups are stored as ZIP files so they can easily be restored from within CR

Full backup is supported for portable, the %appdata% folder for ComicRack & ComicRack CE. Folder location is autodetected

Backup Manager is integrated in the ComicRack toolbar (1-click backups)

### Known Limitations

The Backup Manager provides two backup modes:

* **"normal"** - it saves the ComicDB.xml file in the data folder as well as the custom thumbnails. This mode runs at each start of ComicRack but can be run manually as well.
* **"full"** – it saves the complete content of data including subfolders as well as the custom thumbnails.

With ComicRack 0.9.164 and higher you can use shared SQL servers as data sources for your library instead of the ComicDB.xml file (currently MySQL and MS SQL). If you use these server back ends for your library the normal backup mode of the Backup Manager does not make sense. In this case you should use the database backup features in MySQL and MS SQL, resp. But of course you can use the Backup Manager to backup manually.
