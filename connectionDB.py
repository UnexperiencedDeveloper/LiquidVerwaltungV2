import sqlite3

try:
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE aromen (id INTEGER PRIMARY KEY, aroma VARCHAR(40), marke VARCHAR(20),"
                    "menge INTEGER,"
                    "mix INTEGER,"
                    "preis VARCHAR(10),"
                    "geschmack VARCHAR(100),"
                    "bewertung INTEGER )")

    except sqlite3.OperationalError as _error:
        print(_error)
except sqlite3.OperationalError as error:
    print("Verbindungsaufbau zur Datenbank fehlgeschlagen",error)





# Creates new Entry in Table aromen
def createAroma(aroma,marke,menge,mix,preis,geschmack,bewertung):
    if cur.execute("SELECT id FROM aromen WHERE aroma=?",(aroma,)).fetchone() == None:
        try:
            cur.execute("INSERT INTO aromen (aroma,marke,menge,mix,preis,geschmack,bewertung) VALUES"
                    "(?,?,?,?,?,?,?)",(aroma,marke,menge,mix,preis,geschmack,bewertung))

            con.commit()
        except sqlite3.OperationalError as error:
            print("Daten schreiben fehlgeschlagen",error)
    else:
        print("Aroma Bereits vorhanden")

# Delets the Aroma
def deleteAroma(aroma):
    cur.execute("DELETE FROM aromen WHERE aroma=?",(aroma,))
    con.commit()

# Updates Preis and Menge From Aroma
def updateAroma(aroma,menge,bewertung="",preis=""):
    if preis: # Sobald Preis gesetzt ist, ist auch Bewertung gesetzt
        try:
            cur.execute("UPDATE aromen SET menge=?,preis=?,bewertung=? WHERE aroma=?",(menge,preis,bewertung,aroma))
            con.commit()
        except sqlite3.OperationalError as error:
            print(error)
    elif not bewertung: # Nur Menge Updaten
        try:
            cur.execute("UPDATE aromen SET menge=? WHERE aroma=?",(menge,aroma))
            con.commit()
        except sqlite3.OperationalError as error:
            print(error)
    else:
        try:
            cur.execute("UPDATE aromen SET menge=?,bewertung=?WHERE aroma=?",(menge,bewertung,aroma))
            con.commit()
        except sqlite3.OperationalError as error:
            print(error)

            
# Returns ALL entrys of the Table aromen
def getAromen():
    data = cur.execute("SELECT aroma FROM aromen")
    return data.fetchall()

# Returns all Attributes of given Aroma
def getAttributes(aroma):
    data = cur.execute("SELECT aroma,marke,menge,mix,preis,geschmack,bewertung FROM aromen WHERE aroma =?",(aroma,))

    return data.fetchone()

# Returns a List with Aromen which starts with given Letter
def searchAroma(aroma):
    searchString = "%" + aroma + "%"

    data = cur.execute("SELECT aroma FROM aromen WHERE aroma LIKE ?",(searchString,))
    return data.fetchall()

