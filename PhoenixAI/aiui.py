

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aiui(object):
    def setupUi(self, aiui):
        aiui.setObjectName("aiui")
        aiui.resize(789, 600)
        self.centralwidget = QtWidgets.QWidget(aiui)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, 0, 851, 601))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("D://Projects//Coding//PhoenixAI//1.gif"))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 131, 131))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("D://Projects//Coding//PhoenixAI//2.gif"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(320, 40, 171, 91))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("D://Projects//Coding//PhoenixAI//3.gif"))
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 400, 191, 191))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("D://Projects//Coding//PhoenixAI//5.gif"))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(560, 390, 221, 201))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("D://Projects//Coding//PhoenixAI//6.gif"))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 540, 75, 31))
        font = QtGui.QFont()
        font.setFamily("Aparajita")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(0, 136, 255);\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 540, 75, 31))
        font = QtGui.QFont()
        font.setFamily("Aparajita")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 136, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(560, 30, 111, 41))
        self.textBrowser.setStyleSheet("Background: transparent;\n"
"border-radius: none;\n"
"color: white;\n"
"font-size: 20px;")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(670, 30, 121, 41))
        self.textBrowser_2.setStyleSheet("Background: transparent;\n"
"border-radius: none;\n"
"color: white;\n"
"font-size: 20px;")
        self.textBrowser_2.setObjectName("textBrowser_2")
        aiui.setCentralWidget(self.centralwidget)

        self.retranslateUi(aiui)
        QtCore.QMetaObject.connectSlotsByName(aiui)

    def retranslateUi(self, aiui):
        _translate = QtCore.QCoreApplication.translate
        aiui.setWindowTitle(_translate("aiui", "PhoenixAI"))
        self.pushButton.setText(_translate("aiui", "RUN"))
        self.pushButton_2.setText(_translate("aiui", "EXIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    aiui = QtWidgets.QMainWindow()
    ui = Ui_aiui()
    ui.setupUi(aiui)
    aiui.show()
    sys.exit(app.exec_())
