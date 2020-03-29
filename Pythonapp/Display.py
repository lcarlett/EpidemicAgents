from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence, QGuiApplication, QCursor, QPixmap
from StartOptionsDialog import StartOptionsDialog
from movingGrid import Grid as MovingGrid
from staticHexGrid import Grid as StaticHexGrid
from staticNetwork import Network
from Desease import Desease, DeseasePlot
import os

GRIDS = {"Static Grid":StaticHexGrid, "Moving Grid":MovingGrid, "Small-world Network":Network}
CANVAS_SIZE = (600, 600)

class Display(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUi()
        self.dialog = StartOptionsDialog(self)
        self.dialog.discrete.connect(self.handleDiscrete)
        self.dialog.continuous.connect(self.handleContinuous)
        self.dialog.rejected.connect(self.handleClosedDialog)
        self.start_action.triggered.connect(self.handleNew)
        self.dialog.show()
        self.canvas = None
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.toolBar = super().addToolBar('Settings')
        self.start_action = self.toolBar.addAction('Start')
        self.start_action.setToolTip("Start new simulation")
        self.start_action.setText("New")
        self.start_action.setShortcut(QKeySequence("Ctrl+N"))
        quit_action = self.toolBar.addAction('Quit')
        quit_action.setToolTip("Quit")
        quit_action.setText("Quit")
        quit_action.setShortcut(QKeySequence("Ctrl+W"))
        quit_action.triggered.connect(self.close)
        self.show()
     
    def handleClosedDialog(self):
        if self.canvas:
           self.canvas.startAnimate()
    
    def handleContinuous(self, dic):
        self.setFixedSize(QSize(CANVAS_SIZE[0]*1.1, CANVAS_SIZE[1]*1.1))
        with open("Matlabsim/values.txt", 'w') as values:
            values.write(str(dic["name"])+"\n")
            values.write(str(0.002)+"\n")                               # Birth rate
            values.write(str(0.001)+"\n")                               # Death rate
            values.write(str(dic["grid"]["number_agents"])+"\n")        # Initial population
            values.write(str(dic["desease"]["infectivity"])+"\n")       # Force of infection
            values.write(str(dic["desease"]["recoverability"])+"\n")    # Recovery rate
            values.write(str(1-dic["desease"]["immunity_rate"])+"\n")   # Immunization loss rate
            values.write(str(dic["grid"]["base_infected"])+"\n")        # Initial number of ill
            values.write(str(dic["grid"]["base_immune"])+"\n")          # Initial number of immunized
        os.system("octave --path Matlabsim/ Matlabsim/Models.m")
        centralWidget = QLabel()
        centralWidget.setScaledContents(True)
        centralWidget.setPixmap(QPixmap("Pythonapp/img/result.png"))
        self.setCentralWidget(centralWidget)
        
    def handleNew(self):
        if self.canvas:
            self.canvas.stopAnimate()
        self.dialog.show()
        
    def handleDiscrete(self, dic):
        pause_action = None
        if not self.canvas:
            pause_action = self.toolBar.addAction('Pause')
            pause_action.setToolTip("Pause Simulation")
            pause_action.setText("Pause")
            pause_action.setShortcut(QKeySequence("P"))
            play_action = self.toolBar.addAction('Play')
            play_action.setToolTip("Resume Simulation")
            play_action.setText("Play")
            play_action.setShortcut(QKeySequence("R"))
        QGuiApplication.setOverrideCursor(QCursor(Qt.WaitCursor));
        self.setFixedSize(QSize(CANVAS_SIZE[0]*1.1, CANVAS_SIZE[1]*1.4*1.1))
        centralWidget = QWidget()
        self.canvas = GRIDS[dic["name"]](**(dic["grid"]), size = CANVAS_SIZE, QParent = None, desease = Desease(**(dic["desease"])))
        self.plot = DeseasePlot((CANVAS_SIZE[0], CANVAS_SIZE[1]/3), dic["grid"]["number_agents"])
        self.canvas.startAnimate()
        self.canvas.timeStep.connect(self.plot.updatePlot)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.plot)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        QGuiApplication.restoreOverrideCursor();
        if pause_action:
            pause_action.triggered.connect(self.canvas.stopAnimate)
            play_action.triggered.connect(self.canvas.startAnimate)    
