import sys
sys.path.insert(1,"Display/")
from ui_StartOptionsDialog import Ui_StartOptionsDialog
from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from AbstractGrid import AbstractGrid
from examples import examples

IMAGES = {"Static Grid": "img/static.png", "Moving Grid": "img/moving.png", "Small-world Network": "img/network.png"}
CANVAS_SIZE = (600, 600)

def getExecutable(func, *args):
    return lambda: func(*args)

class NotFilledFormError(Exception):
    def __init__(self, msg = ""):
        super().__init__(msg)

class StartOptionsDialog(QDialog):
    discrete = pyqtSignal(dict)
    continuous = pyqtSignal(dict)
    
    def __init__(self, QParent):
        super().__init__(QParent)
        self.ui = Ui_StartOptionsDialog()
        self.ui.setupUi(self)
        for index in range(len(examples)):
            name = examples[index][0]
            values = examples[index][1]
            temp = QPushButton(name)
            self.ui.examples_layout.addWidget(temp, index%3, index//3)
            temp.pressed.connect(getExecutable(self.setValues, values))
    
    def accept(self):
        self.discrete_go_pressed()
    
    def createDict(self, need_struc):
        desease = {}
        grid = {}
        choosen_struc = str(self.ui.structure_combo.currentText())
        if need_struc and choosen_struc == "Structure":
            raise NotFilledFormError()
        elif choosen_struc == "Moving Grid":
            desease["infectionRadius"] = int((CANVAS_SIZE[0]*CANVAS_SIZE[1]*self.ui.links_spinbox.value()/(3*self.ui.agents_spinbox.value()))**(1/2))
        elif choosen_struc == "Small-world Network":
            grid["base_connections"] = int(self.ui.links_spinbox.value()/2)
            grid["rewiring"] = .1
        desease["recoverability"] = self.ui.recovery_spinbox.value()
        desease["infectivity"] = self.ui.R0_spinbox.value()/self.ui.links_spinbox.value()
        if self.ui.immunizing_checkbox.checkState() == 0:
            immunity = 0
        elif self.ui.immunizing_checkbox.checkState() == 1:
            immunity = .98
        else:
            immunity = 1
        desease["immunity_rate"] = immunity
        grid["number_agents"] = self.ui.agents_spinbox.value()
        grid["base_infected"] = int(self.ui.infected_slider.value()*self.ui.agents_spinbox.value()/100)
        grid["base_immune"] = int(self.ui.immune_spinbox.value()*self.ui.agents_spinbox.value()/100)
        return {"grid": grid, "desease": desease}
    
    def getValues(self):
        out = {}
        out["R0"] = self.ui.R0_spinbox.value()
        out["recovery"] = self.ui.recovery_spinbox.value()
        out["immune"] = self.ui.immune_spinbox.value()
        out["immunizing"] = self.ui.immunizing_checkbox.checkState()
    
    def load_asked(self):
        pass
        
    def setValues(self, dic):
        if not dic:
            return
        else:
            self.ui.R0_spinbox.setValue(dic["R0"])
            self.ui.recovery_spinbox.setValue(dic["recovery"])
            self.ui.immune_spinbox.setValue(dic["immune"])
            self.ui.immunizing_checkbox.setCheckState(dic["immunizing"])
        
    def structure_selected(self,new_str):
        if str(new_str) == "Static Grid":
            self.ui.links_spinbox.setValue(6)
            self.ui.links_spinbox.setEnabled(False)
        else:
            self.ui.links_spinbox.setEnabled(True)
        if str(new_str) == "Small-world Network":
            self.ui.agents_spinbox.setValue(400)
        else:
            self.ui.agents_spinbox.setValue(1000)
        if str(new_str) == "Structure":
            self.ui.structure_preview_label.setPixmap(QPixmap())
        else:
            self.ui.structure_combo.setStyleSheet("background-color: white; color: black;")
            self.ui.structure_preview_label.setPixmap(QPixmap(IMAGES[str(new_str)]))
            
    def immunizing_state_changed(self, state):
        if state == 0:
            texts = ["No", "SIS model"] 
        elif state == 1:
            texts = ["Partial", "SIRS model"]
        elif state == 2:
            texts = ["Yes", "SIR model"]
        self.ui.yes_no_immunizing_label.setText(texts[0])
        self.ui.model_type_label.setText(texts[1])
    
    def discrete_go_pressed(self):
        try:
            dic = self.createDict(True)
            dic["name"] = str(self.ui.structure_combo.currentText())
            self.discrete.emit(dic)
            super().accept()
        except NotFilledFormError:
            self.ui.structure_combo.setStyleSheet("background-color: rgb(204, 0, 0)")
        
    def continuous_go_pressed(self):
        dic = self.createDict(False)
        dic["grid"]["number_agents"] = 1000000
        dic["name"] = self.ui.immunizing_checkbox.checkState()
        self.continuous.emit(dic)
        super().accept()
        
    def test_desease_pressed(self):
        pass
