from PyQt.QtWidgets import QMainWindow

class Display(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.menuBox = 
        
    def startSimulation(self):    
        self.toolBar = self.addToolBar('Settings')
        start = self.toolBar.addAction('Start over')
