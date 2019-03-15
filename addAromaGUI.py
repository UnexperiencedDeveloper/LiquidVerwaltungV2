import connectionDB
from PyQt5 import QtWidgets, uic


#TODO Platzhalter löschen / Ersetzen
#TODO Aroma hinzufügen -> Eingabe clearen
class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("addaroma.ui", self)
        self.ui.btn_add.clicked.connect(self.addAroma)
        self.ui.btn_delete.clicked.connect(self.deleteAroma)
        self.ui.slider_bewertung.valueChanged.connect(self.sliderChanged)
        self.loadList()


    # When User Changes Slider Value -> LabelText Changes
    def sliderChanged(self):
        self.ui.lbl_sliderValue.setText(str(self.ui.slider_bewertung.value()))


    # Loads/Reloads ListWidget via SQL Query
    def loadList(self):
        list = self.ui.list_aroma
        list.clear()
        data = connectionDB.getAromen()
        for item in data:
            list.addItems(item)


    # Add new Aroma to the Database via SQL-Query
    def addAroma(self):
        aroma = str(self.ui.line_aroma.text())
        marke = str(self.ui.line_marke.text())
        mix = self.ui.combo_mix.currentText()
        menge = self.ui.combo_menge.currentText()
        preis = self.ui.line_preis.text()
        geschmack = str(self.ui.line_geschmack.text())
        bewertung = self.ui.slider_bewertung.value()

        if aroma =="" or marke =="" or preis =="":
            print("Alle Felder ausfüllen") # Testzecke
            QtWidgets.QMessageBox.warning(self, "Achtung", "Alle Felder müssen ausgefüllt sein")
        else:
            connectionDB.createAroma(aroma.title(),marke.title(),menge,mix,preis,geschmack.title(),bewertung)
            self.loadList()

    # Delets the Aroma
    def deleteAroma(self):
        try:
            aroma = self.ui.list_aroma.currentItem().text()
            connectionDB.deleteAroma(aroma)
            self.loadList()
        except AttributeError as error:
            print("Aroma auswählen",error) # Testzwecke
            QtWidgets.QMessageBox.warning(self,"Achtung","Aroma muss ausgewählt sein")