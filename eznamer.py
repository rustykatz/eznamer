# EZNAMER
# BY: RUSSELL WONG
# Purpose: Simple script that does the following
# 1) Takes a given File path to specified folder
# 2) Checks for files with a specified string
# 3) Edits each file name appropriately

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

# for filename in os.listdir():
#     if filename.endswith('.txt'):
#         #
#         print(filename)


def printCommands():
    print("COMMANDS:")
    print("list" + "\t\t\t\t" + "-> Lists all files in current PATH")
    print("ls  " + "\t\t\t\t" + "-> Lists files in current PATH")
    print("cd  " + "\t\t\t\t" + "-> Change PATH")
    print("sbe " + "\t\t\t\t" + "-> Select Files by extention")
    print("rf  " + "\t\t\t\t" + "-> Renames a single files in PATH")
    print("raf " + "\t\t\t\t" + "-> Renames all files in PATH")
    print("help" + "\t\t\t\t" + "-> List commands")
    print("exit" + "\t\t\t\t" + "-> Close Program")


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


def selectByExtention(extension):
    mod = []
    for file in os.listdir():
        if (file.endswith(extension)):
            mod.append(file)
    return mod


def renameFile(oldName, newName):
    print("Renaming '%s' to '%s'..." % (oldName, newName))
    os.rename(oldName, newName)


def main():
    # To Do:
    # Necessary
    # 1) Folder name
    # 2) File names
    # 3) List folders and files
    # 4) Remove specified string
    # 5) Command Loop

    printCommands()
    while True:
        print("Current Directory: " + os.getcwd())

        ucmd = input("Enter a command: ")
        if(ucmd == "list"):
            listAllFiles()

        elif(ucmd == "ls"):
            listCurrDirectory()

        elif(ucmd == "cd"):
            path = input("File Path: ")
            changeDirectory(path)

        elif(ucmd == "sbe"):
            extension = input("File Extention: ")
            sbe = selectByExtention(extension)
            print(sbe)

        elif(ucmd == "rf"):
            oldName = input("Old File Name: ")
            newName = input("New File Name: ")
            renameFile(oldName, newName)

        elif(ucmd == "help"):
            printCommands()

        elif(ucmd == "exit"):
            print("Terminating program.")
            sys.exit(0)

        else:
            print("Please input a valid command")


main()
