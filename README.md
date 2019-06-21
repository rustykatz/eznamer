# Eznamer
Copyright 2019 Russell Wong, All Rights Reserved. Unauthorized copying of this file, via any medium is strictly prohibited.
Written By: RUSSELL WONG

## What is Eznamer? 
Eznamer is a simple and intuitive mass file renaming program. Program navigation is similar to that of a unix terminal where users can navigate folders via commands such as 'ls' and 'cd'. 

## How to Use?
Using this application is as simple as downloading the script and running it locally from your terminal. Please make sure to install the necessary dependencies before running the script which can be found below. 
### Program Navigation:
Use commands 'ls' to list all files in your current folder. Changing to a specific folder or directory can be done by using the 'cd' command followed by the desired folder PATH. I.e. 'cd D:\Folder\FolderInsideAFolder'

### The Stage:
The Stage is a list containing all the files that will be modified are stored. To add items to the Stage users can use the command 'add' or 'adde'. 'add' will add all files in the current working directory that cointain a user given substring while 'adde' will add by user given file extension. 

Removing files can be done by using the 'rm', 'rme', or 'clear' commands. 'rm' removes all files in Stage that contain a user given substring, 'rme' will remove by file extension, and 'clear' will remove all items in Stage.
       
### TIPS:
If you plan on modifying batches of the same file types in a session, set the defualt file extension to use by using the 'setx' command.
This will save you from having to manually set it each time you modify a batch of files. 


## Program Dependencies 
As this program is not currently packaged into a standalone application or executable file, it requires users to download the following PYTHON 3.7 libraries. 

| #  | MODULE |
| ------------- | ------------- |
| 1.  | send2trash |


## Command List: 

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


