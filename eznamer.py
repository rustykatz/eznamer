# ~~~~~ EZNAMER ~~~~~
# Copyright 2020 Russell Wong, All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Written By: RUSSELL WONG
# Written In: Python 3.7



# ~~~~~ What is Eznamer? ~~~~~
# Eznamer is a simple and intuitive bulk file renaming program. 
# This program was built to help rename, and organize terrabytes of photos and videos. 
# It now features a modern GUI built using PyQt.

'''
UPDATE LOG: 
- Integration of PYQT GUI for ease of use - DONE
- Some cmd based commands are no longer necessary with gui, so will be removed - DONE
- cmd functionality preserved in 'eznamer_legacy.py' - DONE
- Swapping to OOP design - DONE
- Core functions - DONE
- Simple UI Test - DONE

IN PROGRESS:
- Ergonomic app layout
- Package into executable
- File Move after rename
- File Deletion
'''

# ~~~~~ This is just so I remember what the library functions do ~~~~~
# shutil.copy(source, destination)
# -> copy file at the path source to dest, both are strings.
# -> If dest is a filename, it will be used as the new name of the copied file
# -> Returns a string of the path of the copied file

# shutil.copytree(source, destination)
# -> Copies entire folder and every sub folder/ file


# Deleting Files and Folders:
# os.unlink(path) -> Will delete file at path
# os.rmdir(path) -> delete folder at path, ** MUST BE EMPTY **
# shutil.rmtree(path) -> will delete folder and all files inside
# -> ** Dangerous** as it's ir-reversible

# SEND2TRASH MODULE COMMANDS:
# send2trash.send2trash('filename')
# Sends files to Recycling Bin
# Prevent any unwanted changes by having a prompt window.
# But im too lazy to add the prompt window lmao

# py -m pip install [Package Name]
# UI REBUILD COMMAND
# pyuic5 -o gui_list.py gui_list.ui

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QListWidget
from PyQt5.QtCore import QFile, QTextStream
from gui_list import Ui_MainWindow
import breeze_resources
import send2trash
import shutil

# CONSTANTS
home = os.getenv("HOME")
DEFAULT_DIRECTORY = "D:\Movies"
DEFAULT_INDEX = "1"
DEFAULT_EXTENSION = ".mkv"

class MyMainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Button Connect
        self.ui.btn_dir_change.clicked.connect(self.clicked_btn_dir_change)
        self.ui.btn_dir_apply.clicked.connect(self.clicked_btn_dir_apply)
        self.ui.btn_filter_apply.clicked.connect(self.clicked_btn_filter_apply)
        self.ui.btn_files_apply.clicked.connect(self.clicked_btn_files_apply)
        self.ui.btn_files_select_all.clicked.connect(self.clicked_btn_files_select_all)
        self.ui.btn_files_deselect.clicked.connect(self.clicked_btn_files_deselect)
        self.ui.btn_files_refresh.clicked.connect(self.clicked_btn_files_refresh)
        self.ui.btn_files_move.clicked.connect(self.clicked_btn_files_move)
        self.ui.btn_files_delete.clicked.connect(self.clicked_btn_files_delete)
        # self.ui.btn_files_delete_undo.clicked.connect(self.clicked_btn_files_undo)

        # Defaults 
        self.ui.line_index.setText(DEFAULT_INDEX)
        self.ui.line_extension.setText(DEFAULT_EXTENSION)

    '''
    SECTION 1: DIRECTORY 
    '''
    def clicked_btn_dir_change(self):
        # Try to get default dir opened
        try:
            os.chdir(DEFAULT_DIRECTORY)
        except:
            os.getcwd()
        directory = QFileDialog.getExistingDirectory(self, "Open a folder", home, QFileDialog.ShowDirsOnly)
        self.ui.line_directory.setText(directory)
        # Auto refresh list
        self.clicked_btn_dir_apply()
    
    def clicked_btn_dir_apply(self):
        # Clear list before selection
        self.ui.listWidget.clear() 

        path = self.ui.line_directory.text()
        if path == "": return None  
        os.chdir(path)
        # print(f'Changing to File Path: {path}')
        substr = self.ui.line_filter.text()
        res = selectBySubStr([], substr)

        # Note: Must add 1 to get proper label ->  1. Item ,2. Item
        for i in range(len(res)):
            self.ui.listWidget.addItem(str(i+1) +'. ' + str(res[i]))
            self.ui.listWidget.setHidden(False)
            self.ui.listWidget.item(i).setCheckState(False)  
            # print(self.ui.listWidget.item(i))    

    '''
    SECTION 2: Files
    '''
    # This renames all files in stage 
    def clicked_btn_files_apply(self):
        substr = self.ui.line_filter.text()
        res = selectBySubStr([], substr)
        stage = []

        for i in range(self.ui.listWidget.count()):
            # 0 = unchecked, 2 = checked, 1 = intermediate for trisStates 
            if self.ui.listWidget.item(i).checkState() == 2:
                # stage.append(str(self.ui.listWidget.item(i).text()))
                stage.append(res[i])

        print(stage)

        # Rename all files in stage
        print("Beginning file rename execution...")
        newNames = self.ui.line_name.text()
        fileExtn = self.ui.line_extension.text()
        idx = self.ui.line_index.text()
    
        if newNames != "" and fileExtn != "": 
            # Rename multiple 
            if idx != "": 
                renameFiles(stage, newNames, fileExtn, int(idx))
            else:
                # Rename Single
                renameSingleFile(stage, newNames, fileExtn)
        else:
            print("ERROR: Name, File extension and index cannot be blank.")

 
    # 0 = unchecked, 2 = checked, 1 = intermediate for trisStates 
    def clicked_btn_files_select_all(self):
        for i in range(self.ui.listWidget.count()):
            self.ui.listWidget.item(i).setCheckState(2)

    def clicked_btn_files_deselect(self):
         for i in range(self.ui.listWidget.count()):
            self.ui.listWidget.item(i).setCheckState(0)

    def clicked_btn_files_refresh(self):
        self.clicked_btn_dir_apply()

    def clicked_btn_files_move(self):
        currDir = os.getcwd()
        print(f'Current Directory: {currDir}')

        targetDir = QFileDialog.getExistingDirectory(self, "Open a folder", home, QFileDialog.ShowDirsOnly)
        print(f'Target Directory: {targetDir}')

        substr = self.ui.line_filter.text()
        res = selectBySubStr([], substr)
        stage = []

        for i in range(self.ui.listWidget.count()):
            # 0 = unchecked, 2 = checked, 1 = intermediate for trisStates 
            if self.ui.listWidget.item(i).checkState() == 2:
                # stage.append(str(self.ui.listWidget.item(i).text()))
                stage.append(res[i])

        print(f"Moving Files from {currDir} to {targetDir} ...")
        for files in stage:
            itemLoc = currDir + '\\' + files
            try:
                # print(f"Item Location: {itemLoc}")
                # print(f"Moving Item to {targetDir}")
                shutil.move(itemLoc, targetDir)
            except:
                print(f"ERROR: Moving {files} to {targetDir}. Name already exists at destination.")


    def clicked_btn_files_delete(self):
        substr = self.ui.line_filter.text()
        res = selectBySubStr([], substr)
        stage = []

        for i in range(self.ui.listWidget.count()):
            # 0 = unchecked, 2 = checked, 1 = intermediate for trisStates 
            if self.ui.listWidget.item(i).checkState() == 2:
                # stage.append(str(self.ui.listWidget.item(i).text()))
                stage.append(res[i])

        print("Moving Files to Recycling Bin...")
        deleteFiles(stage)

    # Undo most recent deleted set of files 
    def clicked_btn_files_undo(self):
        pass


    '''
    SECTION 3: SEARCH FILTER
    '''
    def clicked_btn_filter_apply(self):
        substr = self.ui.line_filter.text()
        res = selectBySubStr([], substr)
        # Refresh listwidget list 
        self.ui.listWidget.clear()
        # Note: Must add 1 to get proper label ->  1. Item ,2. Item
        for i in range(len(res)):
            self.ui.listWidget.addItem(str(i+1) +'. ' + str(res[i]))
            self.ui.listWidget.setHidden(False)
            self.ui.listWidget.item(i).setCheckState(False)


''' 
SECTION 4: Utility functions 
'''
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

def renameFiles(stage, newNames, ext, idx):
    total = 0
    for files in os.listdir():
        if(files in stage):
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

def renameSingleFile(stage, newNames, ext):
    if(len(stage) == 1):
        try:
            name = newNames + ext
            print("Renaming '%s' to '%s'..." % (stage[0], name))
            os.rename(stage[0], name)
        except:
            print("ERROR: renameSingleFile-> File name at destination already exists.")
    else:
        print("ERROR: Multiple Files. Please use 'rf' command.")
    print("\n")


def deleteFiles(stage):
    num = 0
    print("Preparing recylcing bin...")
    for files in stage:
        try:
            print("Deleting '%s' from stage... " % (files))
            send2trash.send2trash(files)
            num += 1
        except:
            print("ERROR: Can't delete files")
    print("%s Files successfully deleted." % (num))
    print("\n")



# Handles window switch
class Controller():

    def __init__(self):
        pass

    def show_main(self):
        self.window_main = MyMainWindow()
        #self.window_main.switch_window.connect(self.show_window1)
        self.window_main.show()

def main():
    app = QtWidgets.QApplication(sys.argv)

    # set stylesheet
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
