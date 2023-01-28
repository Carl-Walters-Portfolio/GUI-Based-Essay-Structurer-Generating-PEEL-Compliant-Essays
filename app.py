# from tkinter import W
# from typing_extensions import Self

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtWidgets, QtGui, QtCore

from PyQt6.QtGui import  *
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtMultimedia import *
from PyQt6 import QtMultimedia
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtWidgets

from PyQt6.QtWidgets import (QWidget, QTabWidget, QGridLayout, QApplication, QMainWindow, QStatusBar, QTableView)
from PyQt6.QtCore import (Qt, QTimer, QAbstractTableModel, QThread, QVariant, QObject, QRect, pyqtSlot, pyqtSignal)

import numpy
import os

# x = json.loads(document_name)

import time
import random
import datetime
import json

from CreateData import CreateData
from Files import File
from PEELSorter import PEELSorter

# path = "E:\Brain\Self\dev\Latest2022"

state = True
# emit and threading
#


class WorkerSignals(QObject):
    """ 
    defines and emit signals for a worker thread.
    Args:
        QObject cointains signals
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    """
    Provides event handling for multiple signals to be handled this class is not 
    currently being utilised but would be useful to have from the beginning in anticipation 
    for more complex features.

    Args:
        QRunnable: helps manage a pool of worker threads 
    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        pass    

class MainWindow(QMainWindow):
    """
    MainWindow contains logic that enables and controls various elements within the GUI 
    """
    model = CreateData()
    file = File()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('GUI/' + 'mainwindow.ui', self)
        
        self.submitEntryButton.pressed.connect(lambda: self.addNewEntry())

        self.openFileButton.pressed.connect(lambda: self.setCurrentFile())

        self.entryText.setText("this")

        self.toTextButton.pressed.connect(lambda: self.toText())
        self.currentFile = "file1"
        
        # call count function on start to start with correct count
        self.entryCount = self.countEntries()
        self.setEntryVisual()

    def addNewEntry(self):
        """
        Formats data into a new entry and depends it too data["entry"]
        """
        # select bucket first
        # create new entry from model
        newEntry = self.model.createEmptyEntry()
    
        newEntry["name"] = self.nameInput.text()

        newEntry["number"] = self.countEntries() + 1
            
        newEntry["point"] = self.pointInput.toPlainText()

        #self.pointInput.text() 
        newEntry["Evidence"]["citation"] = self.citationInput.text()

        newEntry["Evidence"]["reference"] = self.referenceinput.text()

        newEntry["Expand"] = self.expandInput.toPlainText()
        newEntry["notes"] = self.notesInput.toPlainText()

        newEntry["link"] = str(self.countEntries() + 1) + ", " + self.linkInput.toPlainText()
        
        # append to correct bucket
        self.appendPEELJson(newEntry)
        
        # no bucket selected
        self.resetInputFields()

    def appendPEELJson(self, aEntry):
        """
        appends aEntry to data["entry"]


        Args:
            aEntry (Json): a single entry containing name, number, point, citation, reference, Expand, notes, link
        """
        data = self.getData(self.currentFile)
        
        data["entry"].append(aEntry)
        
        self.setData(self.currentFile, data)
        

    def resetInputFields(self):
        """
            Resets all of the user input fields ready for a brand new entry
        """
        self.nameInput.clear()
        self.numberInput.clear()
        self.pointInput.clear()
        self.referenceinput.clear()
        self.citationInput.clear()

        self.expandInput.clear()
        self.toInput.clear()
        self.fromInput.clear()
        self.notesInput.clear()
        self.connectTextInput.clear()
        self.linkInput.clear()
        
    def getData(self, fileName):
        """
        Retrieves Jason data from a file.

        Args:
            fileName (Str): Name of file.

        Returns:
            Json: data of the file that was requested 
        """
        data = self.file.readJsonFile(fileName)
        return data
    
    
    def setData(self, name, data):
        """
        Create a json file with the name and data as received.

        Args:
            name (Str): Name of file to be created
            data (Json): relivent data to be stored in file
        """
        dataToWrite = self.file.createJsonfile(self.currentFile, data)
        self.setEntryVisual()

        
    def toText(self):
        """
        Format and create a custom text file containing all of the pure entries in the correct sequence
        """
        data = self.getData(self.currentFile)

        """put in app"""
        text = ""
        
        name = []
        number = []
        point = []
        citation = []
        references = []
        expand = []
        link = []
        notes = []
        
        for entry in data["entry"]:
            name.append(entry["name"])
            number.append(entry["number"])
            point.append(entry["point"])
            citation.append(entry["Evidence"]["citation"])
            references.append(entry["Evidence"]["reference"])
            expand.append(entry["Expand"])
            link.append(entry["link"])
            notes.append(entry["notes"])
            
        pointStr = "POINT \n------------------------------------------------\n"
        evidenceStr = "EVIDENCE\n------------------------------------------------\n"
        expandStr = "EXPAND\n------------------------------------------------\n"
        linkStr = "LINK\n------------------------------------------------\n"
        referenceStr = "REFERENCES\n------------------------------------------------\n"
        
        for index in range(len(data["entry"])):
            """POINT"""
            pointStr += "point " + str(number[index]) + ", "
            pointStr += name[index] + "\n"
            pointStr += point[index] + "\n\n"

            """EVIDENCE"""  
            evidenceStr += "evidence " + str(number[index]) + ", "
            evidenceStr += name[index] + "\n"
            evidenceStr += citation[index] + "\n\n"

            """EXPAND"""
            expandStr += "Expand " + str(number[index]) + ", " + name[index] + "\n"
            expandStr += expand[index] + "\n\n"

            """LINK"""
            linkStr += "Link " + str(number[index]) + ", " + name[index] + "\n"
            linkStr += link[index] + "\n\n"

            """REFERENCE"""
            referenceStr += "reference " + str(number[index]) + ": \n"
            referenceStr += references[index] + "\n\n"

        text = pointStr + "\n\n\n\n" + evidenceStr + "\n\n\n\n" + expandStr + "\n\n\n\n" + linkStr + "\n\n\n\n" + referenceStr
        
        print(text)
        """8 use app version of this"""

        #self.file.createTextFile("complete", text)
        """format"""
        self.file.createTextFile("complete", text)
        
    def countEntries(self):
        """
        Establishes how many entries data["entry"] contains.

        Returns:
            int: number of entries with in data["entry"]
        """
        data = self.getData(self.currentFile)
        count = 0
        count += len(data["entry"])
        
        return count
    
    def setEntryVisual(self):
        """
        Display the number and name of each individual PEEL entry visually in the GUI.
        """
        data = self.getData(self.currentFile)
        self.entrieCounterText.setText(str(len(data["entry"])))
        
        entryTable = ""
        
        for entry in data["entry"]:
            entryTable += str(entry["number"]) + ", " + entry["name"] + "\n"

        self.entryText.setText(entryTable)
                                              
                                               
    def setCurrentFile(self):
        """
        Sets the value of self.currentFile this ferible represents the current filename which contains all of the PEEL entries.
        """
        fileName = self.setFileInput.text()
        self.currentFile = fileName
    
import sys
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
state = False


