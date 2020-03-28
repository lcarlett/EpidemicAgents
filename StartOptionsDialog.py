import sys
sys.path.append("Display/")
from ui_StartOptionsDialog import Ui_StartOptionsDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from AbstractGrid import AbstractGrid

IMAGES = {"Static Grid": "img/static.png", "Moving Grid": "img/moving.png", "Small-world Network": "img/network.png"}
CANVAS_SIZE = (600, 600)
PREVIOUS = {}

class NotFilledFormError(Exception):
    def __init__(self, msg = ""):
        super().__init__(msg)

class StartOptionsDialog(QDialog):
    discrete = pyqtSignal(dict)
    
    def __init__(self, QParent):
        super().__init__(QParent)
        self.ui = Ui_StartOptionsDialog()
        self.ui.setupUi(self)
#        self.setValues(PREVIOUS)
    
    def accept(self):
#        PREVIOUS = self.getValues()
        super().accept()
    
    def reject(self):
#        PREVIOUS = self.getValues()
        super().accept()
    
    def createDict(self):
        desease = {}
        grid = {}
        choosen_struc = str(self.ui.structure_combo.currentText())
        if choosen_struc == "Structure":
            raise NotFilledFormError()
        elif choosen_struc == "Moving Grid":
            desease["infectionRadius"] = int((CANVAS_SIZE[0]*CANVAS_SIZE[1]*self.ui.links_spinbox.value()/(3*self.ui.agents_spinbox.value()))**(1/2))
        elif choosen_struc == "Small-world Network":
            grid["base_connections"] = int(self.ui.links_spinbox.value()/2)
            grid["rewiring"] = .1
        desease["recoverability"] = self.ui.recovery_spinbox.value()
        desease["infectivity"] = self.ui.R0_spinbox.value()/self.ui.links_spinbox.value()
        desease["immunity"] = self.ui.immunizing_checkbox.isChecked()
        grid["number_agents"] = self.ui.agents_spinbox.value()
        grid["base_infected"] = self.ui.infected_slider.value()
        grid["base_immune"] = int(self.ui.immune_spinbox.value()*self.ui.agents_spinbox.value()/100)
        return {"name": choosen_struc, "grid": grid, "desease": desease}
    
    def getValues(self):
        out = {}
        out["R0_spinbox"] = self.ui.R0_spinbox.value()
        out["recovery_spinbox"] = self.ui.recovery_spinbox.value()
        out["immune_spinbox"] = self.ui.immune_spinbox.value()
        out["immunizing_checkbox"] = self.ui.immunizing_checkbox.isChecked()
    
    def load_asked(self):
        pass
        
    def setValues(self, dic):
        if not dic:
            return
        else:
            self.ui.R0_spinbox.setValue(dic["R0_spinbox"])
            self.ui.recovery_spinbox.setValue(dic["recovery_spinbox"])
            self.ui.immune_spinbox.setValue(dic["immune_spinbox"])
            self.ui.immunizing_checkbox.setChecked(dic["immunizing_checkbox"])
        
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
            
    def discrete_go_pressed(self):
        try:
            self.discrete.emit(self.createDict())
            self.accept()
        except NotFilledFormError:
            self.ui.structure_combo.setStyleSheet("background-color: rgb(204, 0, 0)")
        
    def continuous_go_pressed(self):
        emit(self.accept())
        
    def test_desease_pressed(self):
        pass
