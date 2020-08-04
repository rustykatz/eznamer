# Ez-Namer
Copyright 2020 Russell Wong, All Rights Reserved. Unauthorized copying of this file, via any medium is strictly prohibited.

## What is Ez-Namer? 
Ez-Namer is a user friendly bulk file renaming program developed for the purpose of renaming terrabytes of photos and videos easily. 
It now features a modern GUI built using PyQt. 

## Quick Start
To use Ez-Namer, download the script and run it locally from your terminal. Make sure to install the necessary dependencies before running the script. The dependencies are outlined in the "Program Dependencies" section.

1) Run the python program "eznamer.py" from your terminal
2) Click "Change" beside "Directory" to select a folder containing the files you wish to rename
3) Optionally enter in a search filter and click "Apply" beside "Search Filter" 
4) Select the files you wish to rename in the list window
5) Set the a new file name, starting index, and file extension(".jpeg", ".png", ".mkv", etc.)
6) The selected files are added to the Stage. You can view these files by using 'stage'
7) When you are ready, click "Re-Name Selected Files" 
8) All done! 

## New Features - V.2.0
1) GUI built using PyQT
2) Dark Mode

## In Progress
1) Ergonomic App layout
2) Keyboard shortcuts

## DARK MODE: 
Dark theme used is from BreezeStyleSheets which is a fork of QDarkStyleSheet.

# LEGACY - Ez-Namer (Command line version)
The legacy version of Ez-Namer currently offers more tools but is restricted to the command line, as it does not have a UI. 
Program navigation is similar to that of a unix terminal where users can navigate folders via commands such as 'ls' and 'cd'. 

## LEGACY - Quick Start
To use Ez-Namer Legacy, download the script and run it locally from your terminal. Make sure to install the necessary dependencies before running the script. The dependencies are outlined in the "Program Dependencies" section.

1) Run the python program "eznamer_legacy.py" from your terminal
2) Navigate to the folder directory of choice using 'cd' command
3) Use the 'ls' command to view all the files in the folder 
4) Add the files you wish to modify using 'add' 
5) The selected files are added to the Stage. You can view these files by using 'stage'
6) Use 'rf' to rename files to whatever you like
7) All done! 

## TIPS:
If you plan on modifying batches of the same file types in a session, set the defualt file extension to use by using the 'setx' command.
This will save you from having to manually set it each time you modify a batch of files. 


### The Stage:
The Stage is a list containing all the files that will be modified or stored. To add items to the Stage, users can use the command 'add' or 'adde'. 'add' will add all files in the current working directory that cointain a user given substring while 'adde' will add by user given file extension. 

Removing files can be done by using the 'rm', 'rme', or 'clear' commands. 'rm' removes all files in Stage that contain a user given substring, 'rme' will remove by file extension, and 'clear' will remove all items in Stage.

## LEGACY - Command List: 

| COMMAND  | DESCRIPTION |
| ------------- | ------------- |
| lst  | Lists all branch directories from current folder |
| ls  | Lists files in current folder |
| cd  | Change file directories |
| adde  | Add files to Stage by extention |
| add  | Add files to Stage by char string |
| rsf  | Renames a single files in folder  |
| rf  | Renames all files in Stage  |
| rm  | Removes a file from Stage by string (Case Sensitive)  |
| rme  | Removes all files from Stage by file extension.  |
| stage  | List of modifiable items |
| del  | Delete items in Stage |
| setx  | Set File Extension to use for session |
| clear  | Clears Stage |
| help  | List commands |
| use  | Best practice on using the program |
| exit  | Closes Program |

## LEGACY - Program Dependencies 
As this program is not currently packaged into a standalone application or executable file, it requires users to download the following PYTHON 3.7 libraries. 

| #  | MODULE |
| ------------- | ------------- |
| 1.  | send2trash |

