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


def initAscii():
    print("""
    8########################################################8
    8##  ______ _______   _          __  __ ______ _____   ##8
    8## |  ____|___  / \ | |   /\   |  \/  |  ____|  __ \  ##8
    8## | |__     / /|  \| |  /  \  | \  / | |__  | |__) | ##8
    8## |  __|   / / | . ` | / /\ \ | |\/| |  __| |  _  /  ##8
    8## | |____ / /__| |\  |/ ____ \| |  | | |____| | \ \  ##8
    8## |______/_____|_| \_/_/    \_\_|  |_|______|_|  \_\ ##8
    8##                                                    ##8
    8################### By: Russell Wong ###################8
    8########################################################8
    \n
    TO SEE COMMANDS TYPE: 'help'
    TO LEARN HOW TO USE COMMANDS TYPE: 'use'
    \n""")


def printCommands():
    print("""
    COMMANDS:
    lst  " + "\t\t\t\t" + "-> Lists files and sub directories from current PATH
    ls   " + "\t\t\t\t" + "-> Lists files in current PATH
    cd   " + "\t\t\t\t" + "-> Change PATH
    adde " + "\t\t\t\t" + "-> Select Files by extention
    add  " + "\t\t\t\t" + "-> Select Files by sub string
    rsf  " + "\t\t\t\t" + "-> Renames a single files in PATH
    rf   " + "\t\t\t\t" + "-> Renames all files in PATH
    rm   " + "\t\t\t\t" + "-> Removes a file from stage. (Case Sensitive)
    rme  " + "\t\t\t\t" + "-> Removes all files from stage that have the given file extension.
    stage" + "\t\t\t\t" + "-> Shows list of items to be modified
    sext " + "\t\t\t\t" + "-> Set File Extension to use for session
    clear" + "\t\t\t\t" + "-> Clears array containing modifiable items
    help " + "\t\t\t\t" + "-> List commands
    use  " + "\t\t\t\t" + "-> Best practice on using the program
    exit " + "\t\t\t\t" + "-> Close Program
    \n
    """)


def howToUse():
    print("""
    HOW TO USE EZNAMER")
    ########################################################")
    NAVIGATION:
    -> Use commands 'ls' to list all directories at your current
         location. 'lst' will list all directories and sub-directories
         from your current PATH.
    -> Changing directories can be done by using 'cd' followed by the
         desired PATH. I.e. 'cd D:\Movies\Folder'
    \n
    WHAT IS YOUR STAGE:
    -> Stage is where all the files that will be modified are stored.
         You can add items by using commands 'add' or 'adde'
         and remove by 'rm' or 'rme' or 'clear'.
    \n
    TIPS:
    ########################################################
    MODIFYING SAME FILE TYPES IN SESSION
    -> Use 'sext' to set file extention for session.
         Will save you from having to manually
         set it each time you modify a file.
    \n
    """)


# List files in current Directory tree
def listAllFiles():
    print("Listing all files in current directory tree...")
    try:
        cwd = os.getcwd()
        for folder, subfolders, filenames in os.walk(cwd):
            print('The current folder is ' + folder)

            for subfolder in subfolders:
                print('SUBFOLDER OF ' + folder + ': ' + subfolder)

            for filename in filenames:
                print('FILE INSIDE ' + folder + ': ' + filename)

            print('')
    except:
        print("ERROR: Can't list files in directory tree.")


# List files in current Directory
def listCurrDirectory():
    try:
        print("Listing files in current directory...")
        cd = os.listdir()
        print(cd)
    except:
        print("ERROR: Can't list files in current directory.")
    print("\n")


# Change working directory to path
def changeDirectory(path):
    try:
        os.chdir(path)
    except:
        print("ERROR: Invalid directory.")
    print("\n")


def selectByExtention(arr, extension):
    num = 0
    for file in os.listdir():
        if (file.endswith(extension)):
            try:
                print("Adding file to stage: " + file)
                arr.append(file)
                num += 1
            except:
                print("ERROR: Can't add file to stage.")
    print("%s Files have been added to stage." % (num))
    print("\n")
    return arr


# NOTE: substr is case sensitive
def selectBySubStr(arr, substr):
    num = 0
    for file in os.listdir():
        if (substr in file):
            try:
                print("Adding file to stage: " + file)
                arr.append(file)
                num += 1
            except:
                print("ERROR: Can't add file to stage.")
    print("%s Files have been added to stage." % (num))
    print("\n")
    return arr


def renameSingleFile(mod, newName, ext):
    if(len(mod) == 1):
        try:
            name = newName + ext
            print("Renaming '%s' to '%s'..." % (mod[0], name))
            os.rename(mod[0], name)
        except:
            print("ERROR: File name at destination already exists.")
    else:
        print("ERROR: Multiple Files. Please use 'rf' command.")
    print("\n")


def renameFiles(mod, newNames, ext):
    idx = 1
    total = 0
    for files in os.listdir():
        if(files in mod):
            try:
                if(idx <= 9):
                    name = newNames + ' - 0' + str(idx) + ext
                else:
                    name = newNames + ' - ' + str(idx) + ext
                print("Renaming '%s' to '%s'..." % (files, name))
                os.rename(files, name)
                idx += 1
                total += 1
            except:
                print("ERROR: File name at destination already exists.")
    print("%s/%s Files have been successfully renamed." % (idx, total))
    print("\n")


def removeFromStage(mod, name):
    for file in mod:
        try:
            if (file == name):
                mod.remove(file)
        except:
            print("ERROR: Can't remove file from stage.")
    print("\n")
    return mod


def removeExFromStage(mod, ename):
    for files in mod:
        try:
            if(ename in files):
                mod.remove(files)
        except:
            print("ERROR: No files with that extension.")
    print("\n")
    return mod


def deleteFiles(mod):
    num = 0
    print("Preparing recylcing bin...")
    for files in mod:
        try:
            print("Deleting '%s' from stage... " % (files))
            send2trash.send2trash(files)
            num += 1
        except:
            print("ERROR: Can't delete files")
    print("%s Files successfully deleted." % (num))
    print("\n")


def printStage(mod):
    try:
        print("Showing Stage...")
        idx = 1
        for i in mod:
            print(str(idx) + ' ' + i)
    except:
        print("ERROR: Can't show stage.")
    print("\n")


def clearModList(arr):
    try:
        print("Clearing stage List...")
        temp = []
        arr = temp
    except:
        print("ERROR: Can't clear stage.")
    print("\n")
    return arr


def main():
    initAscii()
    # List used for staging changes
    mod = []
    ext = ""
    # Sets session default file extension
    sesext = ""
    # printCommands()
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
            if(sesext == ""):
                ext = input("File Extension: ")
                newName = input("New File Name: ")
                renameSingleFile(mod, newName, ext)
            else:
                newName = input("New File Name: ")
                renameSingleFile(mod, newName, sesext)
            mod = clearModList(mod)

        elif(ucmd == "rf"):
            if(sesext == ""):
                ext = input("File Extension: ")
                newName = input("New File Names: ")
                renameFiles(mod, newName, ext)
            else:
                newName = input("New File Names: ")
                renameFiles(mod, newName, sesext)
            mod = clearModList(mod)

        elif(ucmd == "rm"):
            rname = input("File to remove from stage: ")
            mod = removeFromStage(mod, rname)

        elif(ucmd == "rme"):
            ename = input("Extention to remove from stage: ")
            mod = removeExFromStage(mod, ename)

        elif(ucmd == "stage"):
            printStage(mod)

        elif(ucmd == "sext"):
            ext = input("Session File Extension: ")
            sesext = ext
            print("SESSION FILE EXTENSION SET TO: " + sesext)

        elif(ucmd == "del"):
            delCheck = input("Are you sure you want to delete files? Y/N: ").upper()
            if(delCheck == "Y"):
                deleteFiles(mod)

        elif(ucmd == "clear"):
            mod = clearModList(mod)

        elif(ucmd == "help"):
            printCommands()

        elif(ucmd == "use"):
            howToUse()

        elif(ucmd == "exit"):
            print("Terminating program.")
            sys.exit(0)

        else:
            print("Please input a valid command")


main()
