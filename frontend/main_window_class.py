from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from util.const import FULL_STAR, EMPTY_STAR
from frontend import main_window_design


class MainWindow(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._connectsignals()

    def _connectsignals(self):
        self.predictButton.clicked.connect(self._predictButton)

    def _predictButton(self):
        #the prediction should be called here with the string read from 
        print("Predicting")
        review = self._readReview()
        if review == "":
            print("No review, stopping!")
            return
        # rating = ppl.predict(process_text(review))
        rating = 3
        self._showPrediction(rating)

    def _showPrediction(self, pred):
        str = FULL_STAR * pred
        str += EMPTY_STAR * (5 - pred)
        self.reviewLabel.setText(str)
        self.thread = None
    
    def _readReview(self):
        return self.reviewText.toPlainText()
    