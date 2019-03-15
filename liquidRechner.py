import sys
import connectionDB
from PyQt5 import QtWidgets, uic, QtCore

class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None, aroma=""):
        super().__init__(parent)
        self.ui = uic.loadUi("liquid_rechner.ui", self)
        print(aroma) # TODO Für Testzwecke

        self.ui.lbl_noaroma.hide()
        self.ui.combo_aroma.currentIndexChanged.connect(self.loadAromaAttributes)
        self.ui.combo_ges_menge.currentIndexChanged.connect(self.calculateAttr)
        self.ui.btn_apply.clicked.connect(self.checkForMl)

        self.loadCombo_Aroma()
        self.preSelectCombo(aroma)



    # Loads Attributes from DB (Mixture)
    def loadAromaAttributes(self):
        currentAroma = self.ui.combo_aroma.currentText()
        self.ui.lbl_mix.setText(str(connectionDB.getAttributes(currentAroma)[3])+"%")

        # After select the Aroma the Calculation starts
        self.calculateAttr()

    # Calculates the Attr for the Liquid
    def calculateAttr(self):
        lbl_base = self.ui.lbl_base_ml
        lbl_aroma = self.ui.lbl_aroma_ml

        lbl_mix = self.ui.lbl_mix.text()
        lbl_mix = str(lbl_mix).split("%")

        # Calculation for neededBase and neededAroma
        gesamtMenge = self.ui.combo_ges_menge.currentText()
        needAroma = int(gesamtMenge) * (int(lbl_mix[0])/100)
        lbl_aroma.setText(str(needAroma)+"ml")
        needBase = int(gesamtMenge) - needAroma
        lbl_base.setText(str(needBase)+"ml")

    # Check if enough Aroma ML available for the picked Liquid
    def checkForMl(self):
        menge = connectionDB.getAttributes(self.ui.combo_aroma.currentText())
        needAroma = str(self.ui.lbl_aroma_ml.text())
        float_Aroma = needAroma.split("ml")

        # IF-Statement to check if Enough Aroma available
        if menge[2] >= float(float_Aroma[0]):
            print("Genug") # Testzwecke
            self.ui.lbl_noaroma.hide()
            neue_Menge = menge[2] - float(float_Aroma[0])

            connectionDB.updateAroma(self.ui.combo_aroma.currentText(), neue_Menge)

        else:
            print("Nicht genug") # Testzwecke
            self.ui.lbl_noaroma.show()
        


    # Sets Index of ComboBox on the Selected Aroma
    def preSelectCombo(self,aroma):
        index = self.ui.combo_aroma.findText(aroma)
        self.ui.combo_aroma.setCurrentIndex(index)

    # Loads the ComboBox Data from DB
    def loadCombo_Aroma(self):
        data = connectionDB.getAromen()
        for aromen in data:
            self.ui.combo_aroma.addItem(aromen[0])



