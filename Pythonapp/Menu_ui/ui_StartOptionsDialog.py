# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StartOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartOptionsDialog(object):
    def setupUi(self, StartOptionsDialog):
        StartOptionsDialog.setObjectName("StartOptionsDialog")
        StartOptionsDialog.resize(607, 482)
        StartOptionsDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(StartOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalGroupBox_4 = QtWidgets.QGroupBox(StartOptionsDialog)
        self.horizontalGroupBox_4.setObjectName("horizontalGroupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalGroupBox_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.immunizing_checkbox = QtWidgets.QCheckBox(self.horizontalGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.immunizing_checkbox.sizePolicy().hasHeightForWidth())
        self.immunizing_checkbox.setSizePolicy(sizePolicy)
        self.immunizing_checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.immunizing_checkbox.setTristate(True)
        self.immunizing_checkbox.setObjectName("immunizing_checkbox")
        self.horizontalLayout_8.addWidget(self.immunizing_checkbox)
        self.yes_no_immunizing_label = QtWidgets.QLabel(self.horizontalGroupBox_4)
        self.yes_no_immunizing_label.setObjectName("yes_no_immunizing_label")
        self.horizontalLayout_8.addWidget(self.yes_no_immunizing_label)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.horizontalGroupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        self.recovery_spinbox = QtWidgets.QDoubleSpinBox(self.horizontalGroupBox_4)
        self.recovery_spinbox.setMaximum(1.0)
        self.recovery_spinbox.setSingleStep(0.01)
        self.recovery_spinbox.setObjectName("recovery_spinbox")
        self.gridLayout_2.addWidget(self.recovery_spinbox, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.horizontalGroupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.R0_spinbox = QtWidgets.QDoubleSpinBox(self.horizontalGroupBox_4)
        self.R0_spinbox.setSingleStep(0.5)
        self.R0_spinbox.setObjectName("R0_spinbox")
        self.gridLayout_2.addWidget(self.R0_spinbox, 0, 2, 1, 1)
        self.immune_spinbox = QtWidgets.QDoubleSpinBox(self.horizontalGroupBox_4)
        self.immune_spinbox.setObjectName("immune_spinbox")
        self.gridLayout_2.addWidget(self.immune_spinbox, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.horizontalGroupBox_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 3, 1, 1, 1)
        self.model_type_label = QtWidgets.QLabel(self.horizontalGroupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.model_type_label.sizePolicy().hasHeightForWidth())
        self.model_type_label.setSizePolicy(sizePolicy)
        self.model_type_label.setObjectName("model_type_label")
        self.gridLayout_2.addWidget(self.model_type_label, 3, 2, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_2)
        self.line_2 = QtWidgets.QFrame(self.horizontalGroupBox_4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_4.addWidget(self.line_2)
        self.groupBox = QtWidgets.QGroupBox(self.horizontalGroupBox_4)
        self.groupBox.setObjectName("groupBox")
        self.examples_layout = QtWidgets.QGridLayout(self.groupBox)
        self.examples_layout.setObjectName("examples_layout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.examples_layout.addItem(spacerItem4, 1, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.examples_layout.addItem(spacerItem5, 0, 1, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout.addWidget(self.horizontalGroupBox_4)
        self.horizontalGroupBox_3 = QtWidgets.QGroupBox(StartOptionsDialog)
        self.horizontalGroupBox_3.setObjectName("horizontalGroupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalGroupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.structure_combo = QtWidgets.QComboBox(self.horizontalGroupBox_3)
        self.structure_combo.setStyleSheet("")
        self.structure_combo.setObjectName("structure_combo")
        self.structure_combo.addItem("")
        self.structure_combo.addItem("")
        self.structure_combo.addItem("")
        self.structure_combo.addItem("")
        self.verticalLayout_5.addWidget(self.structure_combo)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.horizontalGroupBox_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.label_7 = QtWidgets.QLabel(self.horizontalGroupBox_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget = QtWidgets.QWidget(self.horizontalGroupBox_3)
        self.widget.setObjectName("widget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.agents_spinbox = QtWidgets.QSpinBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.agents_spinbox.sizePolicy().hasHeightForWidth())
        self.agents_spinbox.setSizePolicy(sizePolicy)
        self.agents_spinbox.setMinimum(10)
        self.agents_spinbox.setMaximum(1000000)
        self.agents_spinbox.setSingleStep(100)
        self.agents_spinbox.setProperty("value", 1000)
        self.agents_spinbox.setObjectName("agents_spinbox")
        self.verticalLayout_8.addWidget(self.agents_spinbox)
        self.verticalLayout_7.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.horizontalGroupBox_3)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.links_spinbox = QtWidgets.QDoubleSpinBox(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.links_spinbox.sizePolicy().hasHeightForWidth())
        self.links_spinbox.setSizePolicy(sizePolicy)
        self.links_spinbox.setMaximum(10.0)
        self.links_spinbox.setSingleStep(0.25)
        self.links_spinbox.setProperty("value", 4.0)
        self.links_spinbox.setObjectName("links_spinbox")
        self.verticalLayout_9.addWidget(self.links_spinbox)
        self.verticalLayout_7.addWidget(self.widget_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.structure_preview_label = QtWidgets.QLabel(self.horizontalGroupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.structure_preview_label.sizePolicy().hasHeightForWidth())
        self.structure_preview_label.setSizePolicy(sizePolicy)
        self.structure_preview_label.setMinimumSize(QtCore.QSize(50, 50))
        self.structure_preview_label.setText("")
        self.structure_preview_label.setScaledContents(True)
        self.structure_preview_label.setObjectName("structure_preview_label")
        self.horizontalLayout_2.addWidget(self.structure_preview_label)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addWidget(self.horizontalGroupBox_3)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_2 = QtWidgets.QLabel(StartOptionsDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_9.addWidget(self.label_2)
        self.infected_slider = QtWidgets.QSlider(StartOptionsDialog)
        self.infected_slider.setProperty("value", 5)
        self.infected_slider.setOrientation(QtCore.Qt.Horizontal)
        self.infected_slider.setObjectName("infected_slider")
        self.horizontalLayout_9.addWidget(self.infected_slider)
        self.label_8 = QtWidgets.QLabel(StartOptionsDialog)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(StartOptionsDialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.line = QtWidgets.QFrame(StartOptionsDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem8)
        self.pushButton = QtWidgets.QPushButton(StartOptionsDialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_11.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_11)
        self.note_label = QtWidgets.QLabel(StartOptionsDialog)
        self.note_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.note_label.setObjectName("note_label")
        self.horizontalLayout.addWidget(self.note_label)
        self.buttons_widget = QtWidgets.QWidget(StartOptionsDialog)
        self.buttons_widget.setMouseTracking(True)
        self.buttons_widget.setObjectName("buttons_widget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.buttons_widget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.discrete_go_button = QtWidgets.QPushButton(self.buttons_widget)
        self.discrete_go_button.setObjectName("discrete_go_button")
        self.verticalLayout_10.addWidget(self.discrete_go_button)
        self.continuous_go_button = QtWidgets.QPushButton(self.buttons_widget)
        self.continuous_go_button.setMouseTracking(False)
        self.continuous_go_button.setObjectName("continuous_go_button")
        self.verticalLayout_10.addWidget(self.continuous_go_button)
        self.horizontalLayout.addWidget(self.buttons_widget)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(StartOptionsDialog)
        self.structure_combo.currentTextChanged['QString'].connect(StartOptionsDialog.structure_selected)
        self.infected_slider.valueChanged['int'].connect(self.label_8.setNum)
        self.immunizing_checkbox.stateChanged['int'].connect(StartOptionsDialog.immunizing_state_changed)
        self.pushButton.pressed.connect(StartOptionsDialog.reject)
        self.discrete_go_button.pressed.connect(StartOptionsDialog.discrete_go_pressed)
        self.continuous_go_button.pressed.connect(StartOptionsDialog.continuous_go_pressed)
        StartOptionsDialog.accepted.connect(self.discrete_go_button.click)
        QtCore.QMetaObject.connectSlotsByName(StartOptionsDialog)

    def retranslateUi(self, StartOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        StartOptionsDialog.setWindowTitle(_translate("StartOptionsDialog", "New Simulation -- Options"))
        self.horizontalGroupBox_4.setTitle(_translate("StartOptionsDialog", "Desease info"))
        self.immunizing_checkbox.setText(_translate("StartOptionsDialog", "Immunizing desease"))
        self.yes_no_immunizing_label.setText(_translate("StartOptionsDialog", "No"))
        self.label_5.setText(_translate("StartOptionsDialog", "Recovery rate"))
        self.label_6.setText(_translate("StartOptionsDialog", "Percentage of base immune in population"))
        self.label_4.setText(_translate("StartOptionsDialog", "R_0"))
        self.model_type_label.setText(_translate("StartOptionsDialog", "SIS model"))
        self.groupBox.setTitle(_translate("StartOptionsDialog", "Examples"))
        self.horizontalGroupBox_3.setTitle(_translate("StartOptionsDialog", "Population structure"))
        self.structure_combo.setItemText(0, _translate("StartOptionsDialog", "Structure"))
        self.structure_combo.setItemText(1, _translate("StartOptionsDialog", "Static Grid"))
        self.structure_combo.setItemText(2, _translate("StartOptionsDialog", "Moving Grid"))
        self.structure_combo.setItemText(3, _translate("StartOptionsDialog", "Small-world Network"))
        self.label_3.setText(_translate("StartOptionsDialog", "Number of agents"))
        self.label_7.setText(_translate("StartOptionsDialog", "Number of neighbours"))
        self.label_2.setText(_translate("StartOptionsDialog", "Starting outbreak"))
        self.label_8.setText(_translate("StartOptionsDialog", "5"))
        self.label_9.setText(_translate("StartOptionsDialog", "%"))
        self.pushButton.setText(_translate("StartOptionsDialog", "Cancel"))
        self.note_label.setText(_translate("StartOptionsDialog", "Or"))
        self.discrete_go_button.setText(_translate("StartOptionsDialog", "Visualize Discrete Evolution"))
        self.continuous_go_button.setText(_translate("StartOptionsDialog", "Visualize Continuous Solution"))
