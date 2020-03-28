from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QKeySequence, QGuiApplication, QCursor
from StartOptionsDialog import StartOptionsDialog
from movingGrid import Grid as MovingGrid
from staticHexGrid import Grid as StaticHexGrid
from staticNetwork import Network
from Desease import Desease, DeseasePlot

GRIDS = {"Static Grid":StaticHexGrid, "Moving Grid":MovingGrid, "Small-world Network":Network}
CANVAS_SIZE = (600, 600)

class Display(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUi()
        self.dialog = StartOptionsDialog(self)
        self.dialog.discrete.connect(self.handleDiscrete)
        self.start_action.triggered.connect(self.handleNew)
        self.dialog.show()
        self.canvas = None
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(QSize(CANVAS_SIZE[0]*1.1, CANVAS_SIZE[1]*1.4*1.1))
        toolBar = super().addToolBar('Settings')
        self.start_action = toolBar.addAction('Start')
        self.start_action.setToolTip("Start new simulation")
        self.start_action.setText("New")
        self.start_action.setShortcut(QKeySequence("Ctrl+N"))
        quit_action = toolBar.addAction('Quit')
        quit_action.setToolTip("Quit")
        quit_action.setText("Quit")
        quit_action.setShortcut(QKeySequence("Ctrl+W"))
        quit_action.triggered.connect(self.close)
        self.show()
        
    def handleNew(self):
        if self.canvas:
            self.canvas.stopAnimate()
        self.dialog.show()
        
    def handleDiscrete(self, dic):
        QGuiApplication.setOverrideCursor(QCursor(Qt.WaitCursor));
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
        
        
