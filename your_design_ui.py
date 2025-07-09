# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(828, 610)
        font = QtGui.QFont()
        font.setFamily("Serif")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("/* 设置整个主窗口的背景为蓝色 */\n"
"QMainWindow {\n"
"    background-color: #ADD8E6; /* 淡蓝色，你也可以使用其他蓝色，例如 blue, #4682B4 (钢蓝色) 等 */\n"
"}\n"
"\n"
"/* 设置所有 QPushButton 的背景为灰色 */\n"
"QPushButton {\n"
"    background-color: #808080; /* 中灰色 */\n"
"    color: white; /* 按钮文字颜色为白色，以便在灰色背景上清晰可见 */\n"
"    border: 1px solid #666666; /* 添加一个浅灰色的边框 */\n"
"    padding: 5px 10px; /* 增加内边距让按钮看起来更舒适 */\n"
"    border-radius: 5px; /* 圆角边框 */\n"
"}\n"
"\n"
"/* 当鼠标悬停在按钮上时，颜色变深一点（可选） */\n"
"QPushButton:hover {\n"
"    background-color: #696969; /* 稍微深一点的灰色 */\n"
"}\n"
"\n"
"/* 当按钮被按下时，颜色再变深（可选） */\n"
"QPushButton:pressed {\n"
"    background-color: #505050; /* 更深的灰色 */\n"
"}")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_feed_label = QtWidgets.QLabel(self.centralwidget)
        self.video_feed_label.setGeometry(QtCore.QRect(20, 130, 411, 331))
        self.video_feed_label.setObjectName("video_feed_label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(540, 190, 181, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.quit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(21)
        self.quit.setFont(font)
        self.quit.setObjectName("quit")
        self.verticalLayout.addWidget(self.quit)
        self.good = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(21)
        self.good.setFont(font)
        self.good.setObjectName("good")
        self.verticalLayout.addWidget(self.good)
        self.bad = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(21)
        self.bad.setFont(font)
        self.bad.setObjectName("bad")
        self.verticalLayout.addWidget(self.bad)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 40, 291, 81))
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 828, 20))
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
        self.video_feed_label.setText(_translate("MainWindow", "TextLabel"))
        self.quit.setText(_translate("MainWindow", "quit"))
        self.good.setText(_translate("MainWindow", "good"))
        self.bad.setText(_translate("MainWindow", "bad"))
        self.label.setText(_translate("MainWindow", "Crab detection"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
