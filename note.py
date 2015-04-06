#!/usr/bin/env python

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

#http://www.flaticon.com/authors/freepik

class db:
    def __init__(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        fname = "notes.db"
        database = QFile(fname)
        
        lol1 = "rarg"
        lol2 = "frarg"
        lol3 = "warg"
        
        if not database.exists():
            self.con.setDatabaseName(fname)
            self.con.open()
            query = QSqlQuery()
            query.exec_("create table notes "
                    "(id integer primary key autoincrement, "
                    "note_name varchar(30), "
                    "note_link varchar(100), "
                    "note_text varchar(255))")
            
        else:
            self.con.setDatabaseName(fname)
            self.con.open()
            
    def execQuery(self, query_str):
        q = QSqlQuery()
        q.exec_(query_str)
             
class MainWindow(QMainWindow):

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        self.setWindowTitle("Notebook")
        
        self.db = db()
        
        self.createActions()
        self.createNoteView()
        
        self.mainWidget=QWidget(self)
        self.mainLayout = QHBoxLayout(self.mainWidget)
        
        self.mainLayout.addWidget(self.lv)
        self.mainLayout.addWidget(self.textEdit)
        
        self.setCentralWidget(self.mainWidget)

        self.newLetter()
        
    def createNoteView(self):
        self.lv = QListView(self)
        
        self.m = QSqlQueryModel()
        self.m.setQuery("SELECT * FROM notes")
        self.m.setHeaderData(0, Qt.Horizontal, "note_name")
        self.lv.setModel(self.m)
        self.lv.setModelColumn(1)
        
        self.lv.setMinimumSize(200,200)
        self.lv.setMaximumSize(200,1000)
        
        self.lv.setSelectionMode(1)
        self.lv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.lv.clicked.connect(self.updateNoteView)
        
        self.textEdit = QTextEdit()
        self.textEdit.setMinimumSize(200,200)

    def newLetter(self):
        self.textEdit.clear() 

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def updateNoteView(self, index):
        if not index:
            return
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.insertText(self.m.data(self.m.index(index.row(),3)))
        
    def about(self):
        QMessageBox.about(self, "About Dock Widgets",
                "The <b>Dock Widgets</b> example demonstrates how to use "
                "Qt's dock widgets. You can enter your own text, click a "
                "customer to add a customer name and address, and click "
                "standard paragraphs to add them.")

    def createActions(self):
        self.newNoteAct = QAction(QIcon('img/pencil.png'), "New",
                self, shortcut=QKeySequence.New,
                statusTip="Create a new form letter", triggered=self.newLetter)

        self.saveAct = QAction(QIcon('img/star.png'), "&Save...", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the current form letter", triggered=self.undo)

        self.undoAct = QAction(QIcon('img/calendar.png'), "&Undo", self,
                shortcut=QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

        self.quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.fileToolBar = self.addToolBar("Options")
        
        self.fileToolBar.addAction(self.newNoteAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.undoAct)
        
        self.fileToolBar.setMovable(0)

        self.statusBar().showMessage("Ready")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

    
