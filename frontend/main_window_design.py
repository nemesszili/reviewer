# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(689, 470)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1024, 786))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_1.setGeometry(QtCore.QRect(60, 30, 571, 431))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.groupBox_1.setFont(font)
        self.groupBox_1.setObjectName("groupBox_1")
        self.predictButton = QtWidgets.QPushButton(self.groupBox_1)
        self.predictButton.setGeometry(QtCore.QRect(230, 320, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.predictButton.setFont(font)
        self.predictButton.setObjectName("predictButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_1)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 380, 451, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.reviewLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.reviewLabel.setFont(font)
        self.reviewLabel.setText("")
        self.reviewLabel.setTextFormat(QtCore.Qt.RichText)
        self.reviewLabel.setObjectName("reviewLabel")
        self.horizontalLayout.addWidget(self.reviewLabel)
        self.reviewText = QtWidgets.QTextEdit(self.groupBox_1)
        self.reviewText.setGeometry(QtCore.QRect(13, 50, 541, 261))
        self.reviewText.setObjectName("reviewText")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reviewer"))
        self.groupBox_1.setTitle(_translate("MainWindow", "Please write a review in the text field below"))
        self.predictButton.setText(_translate("MainWindow", "Predict"))
        self.label.setText(_translate("MainWindow", " Predicted rating: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

