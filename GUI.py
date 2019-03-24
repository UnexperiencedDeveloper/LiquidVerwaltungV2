import sys
import liquidRechner
import addAromaGUI
import connectionDB
import fillUp
from PyQt5 import QtWidgets, uic,QtCore
from PyQt5.QtGui import QPixmap


version = "0.0.1"

#Bewertung nachträglich ändern -> CHECK

class GUI(QtWidgets.QMainWindow):
    #Placeholder for data in the ListWidget, not the Data in the Table. They can be different
    # If they're different, the Function for loading the List gets active
    old_data_aroma = []
    timer = QtCore.QTimer
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("gui.ui", self)

        # TODO Version Control
        #if version != "0.0.2":
         #   QtWidgets.QMessageBox.about(self,"Achtung","Neue Version verfügbar!")

        # Every 200 MiliSecond CheckForNewAroma get's a active
        GUI.timer = QtCore.QTimer()
        GUI.timer.timeout.connect(self.checkForNewAroma)
        GUI.timer.start(200)

        # Timer for Updating Aroma Attributes
        # Timer-Start is in Function defined
        self.timer_Attr = QtCore.QTimer()
        self.timer_Attr.timeout.connect(self.loadAttributes)

        self.checkForNewAroma()
        self.ui.lbl_noentrys.hide()

        self.ui.btn_affuellen.clicked.connect(self.fillUpWindow)
        self.ui.btn_rechner.clicked.connect(self.liquidRechnerWindow)
        self.ui.actionAroma_hinzuf.triggered.connect(self.addAromaWindow)
        self.ui.actionBeenden.triggered.connect(self.beenden)
        self.ui.line_search.textChanged.connect(self.searchList)

        self.ui.list_aroma.itemActivated.connect(self.loadAttributes)

        # Preselect First Item in List and Load Attributes
        self.ui.list_aroma.setCurrentRow(0)
        self.loadAttributes()



    # Checks for new Aroma and calls Function loadList()
    def checkForNewAroma(self):
        data_aroma = connectionDB.getAromen()
        if data_aroma != GUI.old_data_aroma:
            self.loadList(data_aroma)

    # Loads ListWidget with Aroma Name
    def loadList(self,data):
        list = self.ui.list_aroma
        list.clear()
        for aroma in data:
            list.addItems(aroma)
            GUI.old_data_aroma = data

    # Loads the ListWidget with the Search String
    def searchList(self):
        if self.ui.line_search.text() != "":
            # Stops Timer if User uses the Search
            GUI.timer.stop()
            data = connectionDB.searchAroma(self.ui.line_search.text())
            list = self.ui.list_aroma
            list.clear()

            # Check if Search gets Results
            if data == []:
                self.ui.lbl_noentrys.show()
            else:
                for aroma in data:
                    list.addItems(aroma)
                    self.ui.lbl_noentrys.hide()

        else:
            # Starts Timer, hides Label and Reloads List with new DB Query
            self.ui.lbl_noentrys.hide()
            self.loadList(connectionDB.getAromen())
            GUI.timer.start(200)



    # Loads Attributes of Aroma
    def loadAttributes(self):
        try:
            aroma = self.ui.list_aroma.currentItem().text()
            data = connectionDB.getAttributes(aroma)

            marke = self.ui.lbl_marke
            mix = self.ui.lbl_mixture
            menge = self.ui.lbl_menge
            preis = self.ui.lbl_preis
            geschmack = self.ui.lbl_geschmack


            marke.setText(data[1])
            menge.setText(str(data[2])+"ml")
            mix.setText(str(data[3])+"%")
            preis.setText((data[4]+ "€"))
            geschmack.setText(data[5])
            #bewertung.setText(str(data[6]))
            self.ui.lbl_bewertung.setPixmap(QPixmap("Icons\\{0}_rating".format(str(data[6]))))

            # Start Timer for AutoUpdating Attributes
            self.timer_Attr.start(300)
        except AttributeError:
            print("Nichts ausgewählt, Timer erzeugt den Fehler")
            # TODO Durch Timer wird ein Fehler erzeugt, da kein Item zu bestimmtem ausgewählt ist
        except TypeError:
            print("Nichts ausgewählt, Timer erzeugt den Fehler")

    def fillUpWindow(self):
        try:
            aroma = self.ui.list_aroma.currentItem().text()
            dialog = fillUp.GUI(aroma=aroma)
            dialog.show()
        except Exception:
            print("Aroma muss ausgewählt sein")
            QtWidgets.QMessageBox.warning(self, "Achtung", "Aroma muss ausgewählt sein")

    def addAromaWindow(self):
        dialog = addAromaGUI.GUI()
        dialog.show()

    def liquidRechnerWindow(self):
        try:
            aroma = self.ui.list_aroma.currentItem().text()
            dialog = liquidRechner.GUI(aroma=aroma)
            dialog.show()
        except Exception:
            print("Aroma muss ausgewählt sein")
            QtWidgets.QMessageBox.warning(self, "Achtung", "Aroma muss ausgewählt sein")


    def beenden(self):
        dialog.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = GUI()
    dialog.show()
    sys.exit(app.exec_())
