import sys
sys.path.insert(1,"Display/")
from ui_StartOptionsDialog import Ui_StartOptionsDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from AbstractGrid import AbstractGrid

IMAGES = {"Static Grid": "img/static.png", "Moving Grid": "img/moving.png", "Small-world Network": "img/network.png"}
CANVAS_SIZE = (600, 600)

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
        self.ui.buttons_widget.enterEvent = lambda e: self.aboutToClick(e, True)
        self.ui.buttons_widget.leaveEvent = lambda e: self.aboutToClick(e, False)
    
    def aboutToClick(self, e, entering):
        if entering:
            text = "Note: "
            if self.ui.agents_spinbox.value() > 2000:
                text += "A discrete solution may not be able to handle this much agents"
            elif self.ui.agents_spinbox.value() < 10000:
                text += "\nA continuous solution can handle a lot more agents"
            self.ui.note_label.setText(text)
        else:
            self.ui.note_label.setText("Or")
            
    
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
            immunity = 1 - 1/self.ui.immune_time_slider.value()
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
        out["immune_time"] = self.ui.immune_time_slider.value()
    
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
            self.ui.immune_time_slider.setValue(dic["immune_time"])
        
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
            self.ui.immune_time_slider.setEnabled(False)
            self.ui.model_type_label.setText("SIS model")
        elif state == 1:
            self.ui.immune_time_slider.setEnabled(True)
            self.ui.model_type_label.setText("SIRS model")
        elif state == 2:
            self.ui.immune_time_slider.setEnabled(False)
            self.ui.model_type_label.setText("SIR model")
    
    def discrete_go_pressed(self):
        try:
            dic = self.createDict(True)
            dic["name"] = str(self.ui.structure_combo.currentText())
            self.discrete.emit(dic)
            self.accept()
        except NotFilledFormError:
            self.ui.structure_combo.setStyleSheet("background-color: rgb(204, 0, 0)")
        
    def continuous_go_pressed(self):
        dic = self.createDict(False)
        dic["name"] = self.ui.immunizing_checkbox.checkState()
        self.continuous.emit(dic)
        self.accept()
        
    def test_desease_pressed(self):
        pass
