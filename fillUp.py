from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
import connectionDB

class GUI(QtWidgets.QMainWindow):
    def __init__(self,aroma, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("auffüllen.ui", self)


        self.aroma = aroma
        self.getAttr(self.aroma)

        self.ui.slider_bewertung.valueChanged.connect(self.sliderChanged)
        self.ui.btn_apply.clicked.connect(self.updateAroma)
        self.ui.lbl_aroma.setText(self.aroma)



    def sliderChanged(self):
        sliderValue = self.ui.slider_bewertung.value()
        self.ui.lbl_sliderValue.setPixmap(QPixmap("Icons\\{0}_rating".format(sliderValue)))



    def updateAroma(self):
        aroma = self.ui.lbl_aroma.text()
        preis = self.ui.line_preis.text()
        menge_alt = self.ui.lbl_menge.text()
        menge_neu = float(menge_alt) + int(self.ui.combo_menge.currentText())
        bewertung = int(self.ui.slider_bewertung.value())

        connectionDB.updateAroma(aroma,menge_neu,bewertung,preis)
        self.close()

    def getAttr(self,aroma):
        data = connectionDB.getAttributes(aroma)
        menge = data[2]
        preis = data[4]
        bewertung = data[6]

        self.ui.slider_bewertung.setValue(bewertung)
        sliderValue = self.ui.slider_bewertung.value()
        self.ui.lbl_sliderValue.setPixmap(QPixmap("Icons\\{0}_rating".format(sliderValue)))
        self.ui.lbl_menge.setText(str(menge))
        self.ui.line_preis.setText(str(preis))


