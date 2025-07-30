# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewProjectDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        if not NewProjectDialog.objectName():
            NewProjectDialog.setObjectName(u"NewProjectDialog")
        NewProjectDialog.resize(735, 318)
        self.horizontalLayout_2 = QHBoxLayout(NewProjectDialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.treeWidget = QTreeWidget(NewProjectDialog)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.header().setVisible(False)

        self.horizontalLayout_2.addWidget(self.treeWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(NewProjectDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_structTreePath = QLineEdit(self.groupBox)
        self.lineEdit_structTreePath.setObjectName(u"lineEdit_structTreePath")
        self.lineEdit_structTreePath.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_structTreePath, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_type = QLineEdit(self.groupBox)
        self.lineEdit_type.setObjectName(u"lineEdit_type")
        self.lineEdit_type.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_type, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit_product = QLineEdit(self.groupBox)
        self.lineEdit_product.setObjectName(u"lineEdit_product")
        self.lineEdit_product.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_product, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineEdit_batchNum = QLineEdit(self.groupBox)
        self.lineEdit_batchNum.setObjectName(u"lineEdit_batchNum")
        self.lineEdit_batchNum.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_batchNum, 3, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.lineEdit_caseNum = QLineEdit(self.groupBox)
        self.lineEdit_caseNum.setObjectName(u"lineEdit_caseNum")
        self.lineEdit_caseNum.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_caseNum, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOK = QPushButton(NewProjectDialog)
        self.pushButtonOK.setObjectName(u"pushButtonOK")

        self.horizontalLayout.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QPushButton(NewProjectDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(NewProjectDialog)

        QMetaObject.connectSlotsByName(NewProjectDialog)
    # setupUi

    def retranslateUi(self, NewProjectDialog):
        NewProjectDialog.setWindowTitle(QCoreApplication.translate("NewProjectDialog", u"\u65b0\u5efa\u9879\u76ee", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("NewProjectDialog", u"\u65b0\u5efa\u5217", None));
        self.groupBox.setTitle(QCoreApplication.translate("NewProjectDialog", u"\u5de5\u7a0b\u4fe1\u606f:\u53ea\u7528\u4e8e\u663e\u793a\u5185\u5bb9\uff0c\u8bf7\u9009\u4e2d\u6216\u65b0\u5efa\u5bf9\u5e94\u7ed3\u6784\u6811\u5e76\u53f3\u51fb\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("NewProjectDialog", u"\u4f4d\u7f6e", None))
        self.lineEdit_structTreePath.setText("")
        self.label_2.setText(QCoreApplication.translate("NewProjectDialog", u"\u901a\u7528\u4ee3\u53f7", None))
        self.lineEdit_type.setText("")
        self.label_3.setText(QCoreApplication.translate("NewProjectDialog", u"\u4ea7    \u54c1", None))
        self.lineEdit_product.setText("")
        self.label_4.setText(QCoreApplication.translate("NewProjectDialog", u"\u6279    \u6b21", None))
        self.lineEdit_batchNum.setText("")
        self.label_5.setText(QCoreApplication.translate("NewProjectDialog", u"\u7f16    \u53f7", None))
        self.lineEdit_caseNum.setText("")
        self.pushButtonOK.setText(QCoreApplication.translate("NewProjectDialog", u"\u786e\u5b9a", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("NewProjectDialog", u"\u53d6\u6d88", None))
    # retranslateUi
