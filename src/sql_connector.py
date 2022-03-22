import sqlite3
from sqlite3 import Error

con = sqlite3.connect('KaffeDB.db')
print("opened database successfully")




def createTables():

    
    # Tabell for bruker
    con.execute('''CREATE TABLE Bruker (
    BrukerEpost VARCHAR(50) NOT NULL,
    BrukerPassord VARCHAR(50) NOT NULL,
    Fornavn VARCHAR(50) NOT NULL,
    Etternavn VARCHAR(50) NOT NULL,
    CONSTRAINT BrukerPK PRIMARY KEY(BrukerEpost),
    UNIQUE (BrukerEpost) 

    );''')
    print("Table for \"Bruker\" created succesfully")

    # Tabell for KaffeSmaking
    con.execute('''CREATE TABLE KaffeSmaking (
    KaffeSmakingID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Smaksnotater VARCHAR(200),
    Rangering INTEGER NOT NULL
        CHECK(Rangering >=0 AND Rangering <=10),
    SmaksDato DATE NOT NULL DEFAULT CURRENT_DATE,

    BrukerEpost VARCHAR(50) NOT NULL,
    FerdigBrentKaffeID INTEGER NOT NULL,
    CONSTRAINT KaffeSmakingFK1 FOREIGN KEY (FerdigBrentKaffeID) REFERENCES FerdigBrentKaffe(FerdigBrentKaffeID)
                            ON UPDATE CASCADE ,

    CONSTRAINT KaffeSmakingFK2 FOREIGN KEY (BrukerEpost) REFERENCES Bruker(BrukerEpost)
                            ON UPDATE CASCADE


    );''')
    print("Table for \"Kaffesmaking\" created succesfully")

    # Tabell for ferdigBrentKaffe
    con.execute('''CREATE TABLE FerdigBrentKaffe (
    FerdigBrentKaffeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Brenningsgrad VARCHAR(15) NOT NULL,
    BrentDato DATE NOT NULL DEFAULT CURRENT_DATE,
    Beskrivelse VARCHAR(100),
    Kilopris DOUBLE NOT NULL,
    KaffeNavn VARCHAR(50) NOT NULL,

    BrenneriNavn VARCHAR(50) NOT NULL,
    KaffePartiID INTEGER NOT NULL,
    CONSTRAINT FerdigBrentKaffeFK1 FOREIGN KEY (BrenneriNavn) REFERENCES KaffeBrenneri(BrenneriNavn)
                                ON UPDATE CASCADE,
    CONSTRAINT FerdigBrentKaffeFK1 FOREIGN KEY (KaffePartiID) REFERENCES KaffeParti(KaffePartiID)
                                ON UPDATE CASCADE

    );''')
    print("Table for \"FerdigBrentKaffe\" created succesfully")

    # Tabell for Kaffebrenneri
    con.execute('''CREATE TABLE KaffeBrenneri (
    BrenneriNavn VARCHAR(50) NOT NULL,
    Sted VARCHAR(50) NOT NULL,
    Land VARCHAR(50) NOT NULL,
    CONSTRAINT KaffeBrenneriPK PRIMARY KEY (BrenneriNavn)

    );''')
    print("Table for \"KaffeBrenneri\" created succesfully")

    # Tabell for KaffeParti
    con.execute('''CREATE TABLE KaffeParti (
    KaffePartiID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Innhøstingsår INTEGER NOT NULL
                        CHECK ( Innhøstingsår >= 1900 AND Innhøstingsår <= strftime('%Y',CURRENT_DATE)),
    KiloprisFraGård DOUBLE NOT NULL,

    GårdsNavn VARCHAR(50) NOT NULL,
    MetodeNavn VARCHAR(50),
    

    CONSTRAINT KaffePartiFK2 FOREIGN KEY(GårdsNavn) REFERENCES Gård(GårdsNavn)
                        ON UPDATE CASCADE,
    CONSTRAINT KaffePartiFK3 FOREIGN KEY(MetodeNavn) REFERENCES ForedlingsMetode(MetodeNavn)
                        ON UPDATE CASCADE
    );''')
    print("Table for \"KaffeParti\" created succesfully")

    # Tabell for Gård
    con.execute('''CREATE TABLE Gård (
    Land VARCHAR(25),
    Region VARCHAR(25),
    GårdsNavn VARCHAR(50),
    CONSTRAINT GårdPK PRIMARY KEY (GårdsNavn)
    );''')
    print("Table for \"Gård\" created succesfully")

    # Tabell for KaffeBønne
    con.execute('''CREATE TABLE KaffeBønne (
    KaffeBønneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Art VARCHAR(20),
    Type VARCHAR(50)
    );''')
    print("Table for \"KaffeBønne\" created succesfully")

    # Tabell for Foredlingsmetode
    con.execute('''CREATE TABLE ForedlingsMetode(
    MetodeNavn VARCHAR(50),
    Beskrivelse VARCHAR(100),
    CONSTRAINT ForedlingsMetodePK PRIMARY KEY (MetodeNavn)
    );''')
    print("Table for \"Foredlingsmetode\" created succesfully")

    # Tabell for Dyrket
    con.execute('''CREATE TABLE Dyrket(
    KaffeBønneID VARCHAR(20) NOT NULL,
    GårdsNavn VARCHAR(50) NOT NULL,
    CONSTRAINT DyrketPK PRIMARY KEY (KaffeBønneID,GårdsNavn),
    CONSTRAINT DyrketFK1 FOREIGN KEY (GårdsNavn) REFERENCES Gård(GårdsNavn)
                    ON UPDATE CASCADE ,
    CONSTRAINT DyrketFK2 FOREIGN KEY (KaffeBønneID) REFERENCES KaffeBønne(KaffeBønneID)
                    ON UPDATE CASCADE
    );''')
    print("Table for \"Dyrket\" created succesfully")

    # Tabell for iKaffeParti
    con.execute('''CREATE TABLE iKaffeParti(
    KaffePartiID INTEGER NOT NULL,
    KaffeBønneID INTEGER NOT NULL,
    CONSTRAINT iKaffePartiPK PRIMARY KEY (KaffeBønneID,KaffePartiID),
    CONSTRAINT iKaffePartiFK1 FOREIGN KEY (KaffeBønneID) REFERENCES KaffeBønne(KaffeBønneID)
                        ON UPDATE CASCADE ,
    CONSTRAINT iKaffePartiFK2 FOREIGN KEY (KaffePartiID) REFERENCES KaffeParti(KaffePartiID)
                        ON UPDATE CASCADE
    );''')
    print("Table for \"iKaffeParti\" created succesfully")



createTables()

#Vet ikke om vi trenger denne? TODO
#cursorObj = con.cursor()
