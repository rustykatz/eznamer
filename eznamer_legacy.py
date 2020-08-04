# ~~~~~ EZNAMER ~~~~~
# Copyright 2019 Russell Wong, All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Written By: RUSSELL WONG
# Written In: Python 3.7


# ~~~~~ What is Eznamer? ~~~~~
# Eznamer is a simple and intuitive mass file renaming program.
# Program navigation is similar to that of a unix terminal
# where users can navigate folders via commands such as 'ls' and 'cd'.
# SHUTIL MODULE COMMANDS:


# ~~~~~ This is just so I remember what the library functions do ~~~~~
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
# import shutil
# Safer deletion of files
import send2trash
# Modifying files
import os
import sys


def initAscii():
    print("""
    88########################################################88
    88##  ______ _______   _          __  __ ______ _____   ##88
    88## |  ____|___  / \ | |   /\   |  \/  |  ____|  __ \  ##88
    88## | |__     / /|  \| |  /  \  | \  / | |__  | |__) | ##88
    88## |  __|   / / | . ` | / /\ \ | |\/| |  __| |  _  /  ##88
    88## | |____ / /__| |\  |/ ____ \| |  | | |____| | \ \  ##88
    88## |______/_____|_| \_/_/    \_\_|  |_|______|_|  \_\ ##88
    88##                                                    ##88
    88################### By: Russell Wong ###################88
    88########################################################88
    \n
    TO SEE COMMANDS TYPE: 'help'
    TO LEARN HOW TO USE COMMANDS TYPE: 'use'
    \n""")


def printCommands():
    print("""
    COMMANDS:
    lst    -> Lists all branch directories from current folder
    ls     -> Lists files in current folder
    cd     -> Change file directories
    adde   -> Add files to Stage by extention
    add    -> Add files to Stage by char string
    rsf    -> Renames a single files in Folder
    rf     -> Renames all files in Stage
    rm     -> Removes a file from Stage by string (Case Sensitive)
    rme    -> Removes all files from Stage by file extension.
    stage  -> List of modifiable items
    del    -> Delete items in Stage
    setx   -> Set File Extension to use for session
    clear  -> Clears Stage
    help   -> List commands
    use    -> Best practice on using the program
    exit   -> Close Program
    \n
    """)


def howToUse():
    print("""
    HOW TO USE EZNAMER")
    ########################################################")
    -> PROGRAM NAVIGATION: <-
    Use commands 'ls' to list all files in your current folder.
    Changing to a specific folder or directory can be done by using
    the 'cd' command followed by the desired folder PATH.
    I.e. 'cd D:\Folder\FolderInsideAFolder'
    Changing directories can be done by using 'cd' followed by the
       desired PATH. I.e. 'cd D:\Movies\Folder'
    \n
    -> WHAT IS YOUR STAGE: <-
    The Stage is a list containing all the files that will be modified
    are stored. To add items to the Stage users can use the command 'add'
    or 'adde'. 'add' will add all files in the current working directory
    that cointain a user given substring while 'adde' will add by user given
    file extension.
    \n
    -> TIPS: <-
    If you plan on modifying batches of the same file types in a session, 
    set the defualt file extension to use by using the 'setx' command.
    This will save you from having to manually set it each time you modify 
    a batch of files.
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


def renameFiles(mod, newNames, ext, idx):
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
    print("%s/%s Files have been successfully renamed." % (str(idx-1), total))
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

    """
    LIST OF COMMANDS 
    lst    -> Lists all branch directories from current folder
    ls     -> Lists files in current folder
    cd     -> Change file directories
    adde   -> Add files to Stage by extention
    add    -> Add files to Stage by char string
    rsf    -> Renames a single files in PATH
    rf     -> Renames all files in Stage
    rm     -> Removes a file from Stage by string (Case Sensitive)
    rme    -> Removes all files from Stage by file extension.
    stage  -> List of modifiable items
    del    -> List of modifiable items
    setx   -> Set File Extension to use for session
    clear  -> Clears array containing modifiable items
    help   -> List commands
    use    -> Best practice on using the program
    exit   -> Close Program
    """

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
        # strip() removes trailing and leading spaces
        ucmd = (input("Enter a command: ")).strip()
        # input string -> array elem split by spaces
        ucmd = ucmd.split(' ')

        if(ucmd[0] == "listTree"):
            listAllFiles()

        elif(ucmd[0] == "ls"):
            listCurrDirectory()

        elif(ucmd[0] == "cd"):
            # CASE: 1 Input
            if(len(ucmd) == 1):
                nextDir = (input("File Path: ")).strip()
                changeDirectory(nextDir)

            # CASE: 2 or more inputs
            elif(len(ucmd) >= 2):
                nextDir = ""
                for i in range(1, len(ucmd)):
                    nextDir = nextDir + ' ' + ucmd[i]

                # Remove leading and trailing white spaces
                nextDir = nextDir.strip()
                changeDirectory(nextDir)

        elif(ucmd[0] == "adde"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                ext = (input("File Extension: ")).strip()
                # CASE: user forgets '.' in front of extension
                if(ext[0] != '.'):
                    ext = '.' + ext

            # CASE: 2 inputs
            else:
                # CASE: user forgets '.' in front of extension
                if(ucmd[1][0] != '.'):
                    ext = '.' + ucmd[1]

            sbe = selectByExtention(mod, ext)

        elif(ucmd[0] == "add"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                substring = (input("File Subtring: ")).strip()

            # CASE: 2 inputs
            else:
                substring = ucmd[1]

            selectBySubStr(mod, substring)

        elif(ucmd[0] == "rsf"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                # CASE: no global session extension
                if(sesext == ""):
                    ext = (input("File Extension: ")).strip()
                    newName = (input("New File Name: ")).strip()
                    renameSingleFile(mod, newName, ext)
                else:
                    newName = (input("New File Name: ")).stirp()
                    renameSingleFile(mod, newName, sesext)

            # CASE: 2 inputs
            else:
                newName = ""
                for i in range(1, len(ucmd)):
                    newName = newName + ' ' + ucmd[i]
                newName = newName.strip()
                # CASE: no global session extension
                if(sesext == ""):
                    ext = (input("File Extension: ")).strip()
                    renameSingleFile(mod, newName, ext)
                else:
                    renameSingleFile(mod, newName, sesext)
            # Clear mod list before returning
            mod = clearModList(mod)

        elif(ucmd[0] == "rf"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                # Session file extension set
                if(sesext == ""):
                    ext = (input("File Extension: ")).strip()
                    # Add missing . in front of file extension
                    if(ext[0] != '.'):
                        ext = '.' + ext

                    newName = (input("New File Names: ")).strip()
                    startIndex = (input("Starting Index: ")).strip()
                    # Default start index 
                    if str(startIndex) == "":
                        startIndex = '1'
                    renameFiles(mod, newName, ext, int(startIndex))

                # No session file extension set
                else:
                    newName = (input("New File Names: ")).strip()
                    startIndex = (input("Starting Index: ")).strip()
                    # Default start index 
                    if str(startIndex) == "":
                        startIndex = '1'
                    renameFiles(mod, newName, sesext, int(startIndex))

            # CASE: 2 inputs
            else:
                newName = ""
                for i in range(1, len(ucmd)):
                    newName = newName + ' ' + ucmd[i]
                newName = newName.strip()
                if(sesext == ""):
                    ext = (input("File Extension: ")).strip()
                    # CASE: missing '.' for extension
                    if(ext[0] != '.'):
                        ext = '.' + ext
                    renameFiles(mod, newName, ext, 1)
                else:
                    renameFiles(mod, newName, sesext, 1)

            # Clear mod list before returning
            mod = clearModList(mod)

        elif(ucmd[0] == "rm"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                rname = (input("File to remove from stage: ")).strip()

            # CASE: 2 inputs
            else:
                rname = ucmd[1]

            mod = removeFromStage(mod, rname)

        elif(ucmd[0] == "rme"):
            # CASE: 1 input
            if(len(ucmd) == 1):
                ename = (input("Extention to remove from stage: ")).strip()

            # CASE: 2 inputs
            else:
                ename = ucmd[1]

            mod = removeExFromStage(mod, ename)

        elif(ucmd[0] == "stage"):
            printStage(mod)

        elif(ucmd[0] == "setx"):
            # CASE: 1 inputs
            if(len(ucmd) == 1):
                sesext = (input("Session File Extension: ")).strip()

            # CASE: 2 input
            else:
                sesext = ucmd[1]

            # CASE: Missing '.' for extension
            if(sesext[0] != '.'):
                sesext = '.' + sesext
            print("SESSION FILE EXTENSION SET TO: " + sesext)

        elif(ucmd[0] == "del"):
            delCheck = (input("Are you sure you want to delete files? Y/N: ")).strip().upper()
            if(delCheck == "Y"):
                deleteFiles(mod)

        elif(ucmd[0] == "clear"):
            mod = clearModList(mod)

        elif(ucmd[0] == "help"):
            printCommands()

        elif(ucmd[0] == "use"):
            howToUse()

        elif(ucmd[0] == "exit"):
            print("Terminating program...")
            sys.exit(0)

        else:
            print("Please input a valid command! ")

if __name__ == "__main__":
    main()
