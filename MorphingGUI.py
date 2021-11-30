# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1006, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LoadStarting = QtWidgets.QPushButton(self.centralwidget)
        self.LoadStarting.setGeometry(QtCore.QRect(50, 0, 141, 31))
        self.LoadStarting.setObjectName("LoadStarting")
        self.LoadEnding = QtWidgets.QPushButton(self.centralwidget)
        self.LoadEnding.setGeometry(QtCore.QRect(590, 0, 141, 31))
        self.LoadEnding.setObjectName("LoadEnding")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(190, 370, 591, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.Alphalabel = QtWidgets.QLabel(self.centralwidget)
        self.Alphalabel.setGeometry(QtCore.QRect(136, 370, 51, 20))
        self.Alphalabel.setObjectName("Alphalabel")
        self.zero = QtWidgets.QLabel(self.centralwidget)
        self.zero.setGeometry(QtCore.QRect(190, 390, 61, 31))
        self.zero.setObjectName("zero")
        self.Startlabel = QtWidgets.QLabel(self.centralwidget)
        self.Startlabel.setGeometry(QtCore.QRect(170, 320, 101, 31))
        self.Startlabel.setObjectName("Startlabel")
        self.Endlabel = QtWidgets.QLabel(self.centralwidget)
        self.Endlabel.setGeometry(QtCore.QRect(730, 320, 91, 31))
        self.Endlabel.setObjectName("Endlabel")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(450, 320, 121, 31))
        self.checkBox.setObjectName("checkBox")
        self.StartImage = QtWidgets.QGraphicsView(self.centralwidget)
        self.StartImage.setGeometry(QtCore.QRect(50, 40, 360, 270))
        self.StartImage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.StartImage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.StartImage.setObjectName("StartImage")
        self.BlendImage = QtWidgets.QGraphicsView(self.centralwidget)
        self.BlendImage.setGeometry(QtCore.QRect(310, 400, 360, 270))
        self.BlendImage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.BlendImage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.BlendImage.setObjectName("BlendImage")
        self.EndImage = QtWidgets.QGraphicsView(self.centralwidget)
        self.EndImage.setGeometry(QtCore.QRect(590, 40, 360, 270))
        self.EndImage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.EndImage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.EndImage.setObjectName("EndImage")
        self.one = QtWidgets.QLabel(self.centralwidget)
        self.one.setGeometry(QtCore.QRect(770, 400, 61, 31))
        self.one.setObjectName("one")
        self.Blendlabel = QtWidgets.QLabel(self.centralwidget)
        self.Blendlabel.setGeometry(QtCore.QRect(460, 680, 91, 31))
        self.Blendlabel.setObjectName("Blendlabel")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(800, 370, 101, 51))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 710, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1006, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LoadStarting.setText(_translate("MainWindow", "Load Starting Image..."))
        self.LoadEnding.setText(_translate("MainWindow", "Load Ending Image..."))
        self.Alphalabel.setText(_translate("MainWindow", "Alpha"))
        self.zero.setText(_translate("MainWindow", "0.0"))
        self.Startlabel.setText(_translate("MainWindow", "Starting Image"))
        self.Endlabel.setText(_translate("MainWindow", "Ending Image"))
        self.checkBox.setText(_translate("MainWindow", "show Traigles"))
        self.one.setText(_translate("MainWindow", "1.0"))
        self.Blendlabel.setText(_translate("MainWindow", "Blending Image"))
        self.pushButton_2.setText(_translate("MainWindow", "Blend"))


