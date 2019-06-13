# EZNAMER
# BY: RUSSELL WONG
# Purpose: Simple renaming program that does the following
# 1) Takes a given File path to specified folder
# 2) Checks for files with a specified string
# 3) Adds files that user wants to modify into 'mod' list
# 3) Applys changes

# SHUTIL MODULE COMMANDS:

# shutil.copy(source, destination)
# -> copy file at the path source to dest, both are strings.
# -> If dest is a filename, it will be used as the new name of the copied file
# -> Returns a string of the path of the copied file

# shutil.copytree(source, destination)
# -> Copies entire folder and every sub folder/ file

# shutil.move(source, destination)
# -> Moves file S->D
# -> if filename already exists at D, D file is overwritten by S
# ** Can specify a name at D to rename the S file when moving**
# -> i.e. shutil.move('C:\\file.text', 'C:\\newfilename.text')
# ** if you specify D as a folder,
# make sure to check if it exists or else it will rename S to D
# thinking D is a file name not a folder

# Deleting Files and Folders:
# os.unlink(path) -> Will delete file at path
# os.rmdir(path) -> delete folder at path, ** MUST BE EMPTY **
# shutil.rmtree(path) -> will delete folder and all files inside
# -> ** Dangerous** as it's ir-reversible

# SEND2TRASH MODULE COMMANDS:
# send2trash.send2trash('filename')
# Sends files to Recycling Bin
# Prevent any unwanted changes by printing all files being modified first


# py -m pip install [Package Name]

# Fxns to copy, move, rename and delete files
import shutil
# Safer deletion of files
import send2trash
# Modifying files
import os
import sys
# CURRENT TARGET OS PATH
# D:\Movies\'FolderName'


def printCommands():
    print("COMMANDS:")
    print("lst  " + "\t\t\t\t" + "-> Lists all files in directory tree")
    print("ls   " + "\t\t\t\t" + "-> Lists files in current PATH")
    print("cd   " + "\t\t\t\t" + "-> Change PATH")
    print("adde  " + "\t\t\t\t" + "-> Select Files by extention")
    print("add  " + "\t\t\t\t" + "-> Select Files by sub string")
    print("rsf  " + "\t\t\t\t" + "-> Renames a single files in PATH")
    print("rf   " + "\t\t\t\t" + "-> Renames all files in PATH")
    print("stage" + "\t\t\t\t" + "-> Shows mod list")
    print("clear" + "\t\t\t\t" + "-> Clears array containing modifiable items")
    print("help " + "\t\t\t\t" + "-> List commands")
    print("exit " + "\t\t\t\t" + "-> Close Program")


# List files in current Directory
def listAllFiles():
    print("Listing all files in current directory...")
    cwd = os.getcwd()
    for folder, subfolders, filenames in os.walk(cwd):
        print('The current folder is ' + folder)

        for subfolder in subfolders:
            print('SUBFOLDER OF ' + folder + ': ' + subfolder)

        for filename in filenames:
            print('FILE INSIDE ' + folder + ': ' + filename)

        print('')


def listCurrDirectory():
    print("Listing files in current directory...")
    a = os.listdir()
    print(a)


# Change working directory to path
def changeDirectory(path):
    try:
        os.chdir(path)
    except:
        print("Invalid Directory")


def selectByExtention(arr, extension):
    for file in os.listdir():
        if (file.endswith(extension)):
            print("Adding file: " + file)
            arr.append(file)
    return arr


# NOTE: substr is case sensitive
def selectBySubStr(arr, substr):
    for file in os.listdir():
        if (substr in file):
            print("Adding file: " + file)
            arr.append(file)

    return arr


def renameSingleFile(mod, newName, ext):
    if(len(mod) == 1):
        try:
            name = newName + ext
            print("Renaming '%s' to '%s'..." % (mod[0], name))
            os.rename(mod[0], name)
        except:
            print("ERROR: Cannot create a file when that file already exists.")
    else:
        print("ERROR: Multiple Files. Please use 'rf' command.")


def renameFiles(mod, newNames, ext):
    idx = 1
    for files in os.listdir():
        if(files in mod):
            try:
                name = newNames + ' ' + str(idx) + ext
                print("Renaming '%s' to '%s'..." % (files, name))
                os.rename(files, name)
                idx += 1
            except:
                print("ERROR: Cannot create a file when that file already exists.")


def printStage(mod):
    print("Showing Stage...")
    idx = 1
    for i in mod:
        print(str(idx) + ' ' + i)


def clearModList(arr):
    print("Clearing Mod List...")
    temp = []
    arr = temp
    return arr


def main():
    # List used for staging changes
    mod = []
    ext = ""
    printCommands()
    while True:
        print("Current Directory: " + os.getcwd())

        ucmd = input("Enter a command: ")

        if(ucmd == "listTree"):
            listAllFiles()

        elif(ucmd == "ls"):
            listCurrDirectory()

        elif(ucmd == "cd"):
            path = input("File Path: ")
            changeDirectory(path)

        elif(ucmd == "adde"):
            ext = input("File Extension: ")
            sbe = selectByExtention(mod, ext)

        elif(ucmd == "add"):
            substring = input("File Subtring: ")
            selectBySubStr(mod, substring)

        elif(ucmd == "rsf"):
            ext = input("File Extension: ")
            newName = input("New File Name: ")
            renameSingleFile(mod, newName, ext)
            mod = clearModList(mod)

        elif(ucmd == "rf"):
            ext = input("File Extension: ")
            newName = input("New File Names: ")
            renameFiles(mod, newName, ext)
            mod = clearModList(mod)

        elif(ucmd == "stage"):

            printStage(mod)

        elif(ucmd == "clear"):
            mod = clearModList(mod)

        elif(ucmd == "help"):
            printCommands()

        elif(ucmd == "exit"):
            print("Terminating program.")
            sys.exit(0)

        else:
            print("Please input a valid command")


main()
