### You should consider using [ComicRack Community Edition](https://github.com/maforget/ComicRackCE). And if you can please contribute to the project.

[Download Here](https://github.com/maforget/cr-backup-manager/releases/download/v1.2/CR.Backup.Manager_v1.2.crplugin)

# Backup Manager for ComicRack

docdoom (updated by maforget) Proudly Presents the Backup Manager for ComicRack

This little plugin automates the process of saving the ComicRack library file. See the manual here for further information.

### Changes from original (by maforget)

**v1.3**
* CHANGE - Startup backup will now be done in the background and not freeze the program anymore

**v1.2**
* Added - Added a full backup option on startup & shutdown

**v1.1**
* CHANGE - Made compatible with ComicRack Community Edition, Alternate Config and Portable (will auto detect the data folder location).
    * Unless you do a Full Backup, it will only save the current configuration DB & thumbnails.
* CHANGE - Updated Zip Library to DotNetZip v1.16.0

Backups are stored as ZIP files so they can easily be restored from within CR.

Full backup is supported for portable, the %appdata% folder for ComicRack & ComicRack CE. Folder location is autodetected.

Backup Manager is integrated in the ComicRack toolbar (1-click backups)

### Known Limitations

The Backup Manager provides two backup modes:

* **"normal"** - it saves the ComicDB.xml file in the data folder as well as the custom thumbnails. This mode runs at each start of ComicRack but can be run manually as well.
* **"full"** – it saves the complete content of data including subfolders as well as the custom thumbnails.

With ComicRack 0.9.164 and higher you can use shared SQL servers as data sources for your library instead of the ComicDB.xml file (currently MySQL and MS SQL). If you use these server back ends for your library the normal backup mode of the Backup Manager does not make sense. In this case you should use the database backup features in MySQL and MS SQL, resp. But of course you can use the Backup Manager to backup manually.

----

#### Check my plugins for ComicRack Community Edition:

- **[Android Client](https://github.com/maforget/ComicRackKeygen/releases/tag/1.0). Includes the link to the Android Client. It still work correctly with the Community Edition & still works with the Latest Android 14 (although for 14+ you will need to install via ADB). Also includes stuff like a Keygen & a Support Pack for the Original ComicRack, but those aren't required anymore with the Community Edition anymore.**
- **[Amazon Scrapper](https://github.com/maforget/ComicRack_AmazonScrapper). A Scrapper for Amazon books (former Comixology library).**
- **[Data Manager](https://github.com/maforget/CRDataManager) let's you manipulate your data for ComicRack. Fix the various bugs in the latest v2 release.**
- **[Backup Manager for ComicRack](https://github.com/maforget/cr-backup-manager) Automates the process of saving the ComicRack library file or easy 1 click backup. Updated to support the Community Edition, Portable mode & Alternate Configurations.**
- **[Bédéthèque Scrapper v2](https://github.com/maforget/Bedetheque-Scrapper-2) to scrap data from the French BD site Bédétheque.**
- **[Find Image Resolution](https://github.com/maforget/ComicRack_FindImageResolution) to determine the resolution of a comic. Use it by right-clicking => Automation => Find Image Resolution (.NET). Configuration are in File => Automation => Find Image Resolution (.NET) Config.**
- **[fullscreen.py](https://gist.githubusercontent.com/maforget/186a99205140acd3f7d3328ad1466e62/raw/8c7c0ecab28fb9a6037adbe19ff553e3597cccd6/fullscreen.py). It will automatically fullscreen the application when either opening a book or starting the application depending on which you enable). Copy the file in either `%programfiles%\ComicRack Community Edition\Scripts` or `%appdata%\cYo\ComicRack Community Edition\Scripts`.**
- **[comicrack-copy-move-field](https://github.com/maforget/comicrack-copy-move-field). Moves or copies info from one field to another. Can either replace or append to the destination field. Small update from the original to permit dates to be copied or moved.**
