# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rating.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1150, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(1150, 640))
        Form.setMaximumSize(QtCore.QSize(1150, 640))
        Form.setStyleSheet("QWidget {background-color: #1581e6; color: white; font-family: \"Days\";}\n"
"QHeaderView::section {background-color:rgb(21, 129, 230)}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(-1, 39, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 13)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Days")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignRight)
        self.mode_of_sorting = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mode_of_sorting.sizePolicy().hasHeightForWidth())
        self.mode_of_sorting.setSizePolicy(sizePolicy)
        self.mode_of_sorting.setMinimumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setFamily("Days")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.mode_of_sorting.setFont(font)
        self.mode_of_sorting.setEditable(False)
        self.mode_of_sorting.setFrame(True)
        self.mode_of_sorting.setObjectName("mode_of_sorting")
        self.horizontalLayout_2.addWidget(self.mode_of_sorting)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.rating_table = QtWidgets.QTableWidget(Form)
        self.rating_table.setStyleSheet("QHeaderView { font-size: 16pt; }")
        self.rating_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rating_table.setObjectName("rating_table")
        self.rating_table.setColumnCount(0)
        self.rating_table.setRowCount(0)
        self.verticalLayout.addWidget(self.rating_table)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Претест"))
        self.label.setText(_translate("Form", "Сортировать:"))