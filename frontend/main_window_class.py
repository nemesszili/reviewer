from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from util.const import FULL_STAR, EMPTY_STAR
from util.process import process_text
from frontend import main_window_design

class MainWindow(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self, ppl):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._connectsignals()
        self.ppl = ppl

    def _connectsignals(self):
        self.predictButton.clicked.connect(self._predictButton)

    def _predictButton(self):
        #the prediction should be called here with the string read from 
        review = self._readReview()
        if not review:
            return
        rating = self.ppl.predict(process_text(review))[0]
        self._showPrediction(rating)

    def _showPrediction(self, pred):
        star = FULL_STAR * pred
        star += EMPTY_STAR * (5 - pred)
        self.reviewLabel.setText(star)
        self.thread = None
    
    def _readReview(self):
        return self.reviewText.toPlainText()
    