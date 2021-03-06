import sqlite3
from sqlite3 import Error

con = sqlite3.connect('KaffeDB.db')
print("opened database successfully")



def createTables():

    
    # Tabell for bruker
    con.execute('''CREATE TABLE IF NOT EXISTS Bruker (
    BrukerEpost VARCHAR(50) NOT NULL,
    BrukerPassord VARCHAR(50) NOT NULL,
    Fornavn VARCHAR(50) NOT NULL,
    Etternavn VARCHAR(50) NOT NULL,
    CONSTRAINT BrukerPK PRIMARY KEY(BrukerEpost),
    UNIQUE (BrukerEpost) 

    );''')
    print("Table for \"Bruker\" created succesfully")

    # Tabell for KaffeSmaking
    con.execute('''CREATE TABLE IF NOT EXISTS KaffeSmaking (
    KaffeSmakingID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Smaksnotater VARCHAR(200),
    Rangering INTEGER NOT NULL
        CHECK(Rangering >=0 AND Rangering <=10),
    SmaksDato DATE NOT NULL DEFAULT CURRENT_DATE,

    BrukerEpost VARCHAR(50) NOT NULL,
    FerdigBrentKaffeID INTEGER NOT NULL,
    CONSTRAINT KaffeSmakingFK1 FOREIGN KEY (FerdigBrentKaffeID) REFERENCES FerdigBrentKaffe(FerdigBrentKaffeID)
                            ON UPDATE CASCADE,

    CONSTRAINT KaffeSmakingFK2 FOREIGN KEY (BrukerEpost) REFERENCES Bruker(BrukerEpost)
                            ON UPDATE CASCADE


    );''')
    print("Table for \"Kaffesmaking\" created succesfully")

    # Tabell for ferdigBrentKaffe
    con.execute('''CREATE TABLE IF NOT EXISTS FerdigBrentKaffe (
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
    con.execute('''CREATE TABLE IF NOT EXISTS KaffeBrenneri (
    BrenneriNavn VARCHAR(50) NOT NULL,
    Sted VARCHAR(50) NOT NULL,
    BrenneriLand VARCHAR(50) NOT NULL,
    CONSTRAINT KaffeBrenneriPK PRIMARY KEY (BrenneriNavn)

    );''')
    print("Table for \"KaffeBrenneri\" created succesfully")

    # Tabell for KaffeParti
    con.execute('''CREATE TABLE IF NOT EXISTS  KaffeParti (
    KaffePartiID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Innh??stings??r INTEGER NOT NULL
                        CHECK ( Innh??stings??r >= 1900 AND Innh??stings??r <= strftime('%Y',CURRENT_DATE)),
    KiloprisFraG??rd DOUBLE NOT NULL,

    G??rdsNavn VARCHAR(50) NOT NULL,
    MetodeNavn VARCHAR(50),
    

    CONSTRAINT KaffePartiFK2 FOREIGN KEY(G??rdsNavn) REFERENCES G??rd(G??rdsNavn)
                        ON UPDATE CASCADE,
    CONSTRAINT KaffePartiFK3 FOREIGN KEY(MetodeNavn) REFERENCES ForedlingsMetode(MetodeNavn)
                        ON UPDATE CASCADE
    );''')
    print("Table for \"KaffeParti\" created succesfully")

    # Tabell for G??rd
    con.execute('''CREATE TABLE IF NOT EXISTS G??rd (
    Land VARCHAR(25),
    Region VARCHAR(25),
    G??rdsNavn VARCHAR(50),
    Moh int NOT NULL,
    CONSTRAINT G??rdPK PRIMARY KEY (G??rdsNavn)
    );''')
    print("Table for \"G??rd\" created succesfully")

    # Tabell for KaffeB??nne
    con.execute('''CREATE TABLE IF NOT EXISTS  KaffeB??nne (
    KaffeB??nneID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    Art VARCHAR(20),
    Type VARCHAR(50)
    );''')
    print("Table for \"KaffeB??nne\" created succesfully")

    # Tabell for Foredlingsmetode
    con.execute('''CREATE TABLE IF NOT EXISTS ForedlingsMetode(
    MetodeNavn VARCHAR(50),
    Beskrivelse VARCHAR(100),
    CONSTRAINT ForedlingsMetodePK PRIMARY KEY (MetodeNavn)
    );''')
    print("Table for \"Foredlingsmetode\" created succesfully")

    # Tabell for Dyrket
    con.execute('''CREATE TABLE IF NOT EXISTS Dyrket(
    KaffeB??nneID VARCHAR(20) NOT NULL,
    G??rdsNavn VARCHAR(50) NOT NULL,
    CONSTRAINT DyrketPK PRIMARY KEY (KaffeB??nneID,G??rdsNavn),
    CONSTRAINT DyrketFK1 FOREIGN KEY (G??rdsNavn) REFERENCES G??rd(G??rdsNavn)
                    ON UPDATE CASCADE ,
    CONSTRAINT DyrketFK2 FOREIGN KEY (KaffeB??nneID) REFERENCES KaffeB??nne(KaffeB??nneID)
                    ON UPDATE CASCADE
    );''')
    print("Table for \"Dyrket\" created succesfully")

    # Tabell for iKaffeParti
    con.execute('''CREATE TABLE IF NOT EXISTS iKaffeParti(
    KaffePartiID INTEGER NOT NULL,
    KaffeB??nneID INTEGER NOT NULL,
    CONSTRAINT iKaffePartiPK PRIMARY KEY (KaffeB??nneID,KaffePartiID),
    CONSTRAINT iKaffePartiFK1 FOREIGN KEY (KaffeB??nneID) REFERENCES KaffeB??nne(KaffeB??nneID)
                        ON UPDATE CASCADE ,
    CONSTRAINT iKaffePartiFK2 FOREIGN KEY (KaffePartiID) REFERENCES KaffeParti(KaffePartiID)
                        ON UPDATE CASCADE
    );''')
    print("Table for \"iKaffeParti\" created succesfully")

def fillDummyData():
    con.execute('''
    INSERT INTO KaffeBrenneri(BrenneriNavn, Sted, BrenneriLand)
    VALUES
        ("Lang??ra Brenneri", "Trondheim", "Norge"),
        ("Jacobsen og svart", "Aarhus", "Danmark"),
        ("Hringariki", "Bogota", "Colombia");''')
    
    

    con.execute('''
    INSERT INTO Foredlingsmetode(MetodeNavn, Beskrivelse)
    VALUES
    ("T??rket", "T??rker kaffeb??nnene"),
    ("Vasket", "Vasker kaffeb??nnene"),
    ("B??rt??rket", "T??rket p?? b??r");''')

    con.execute('''
    INSERT INTO G??rd(G??rdsNavn, Land, Region, Moh)
    VALUES
    ("El Cherro", "Spania", "Aragon", 1200),
    ("Malta", "Colombia", "Andes", 500),
    ("Nombre de Dios", "El Salvador", "Santa Ana", 1500);''')

    con.execute('''
    INSERT INTO KaffeB??nne(Art, Type)
    VALUES
    ("Bourbon", "Arabica"), 
    ("Excelsa", "Liberica"), 
    ("Asterids", "Liberica");''') #1,2,3

    con.execute('''
    INSERT INTO KaffeParti(Innh??stings??r, KiloprisFraG??rd, G??rdsNavn, MetodeNavn)
    VALUES 
    (2021, 80, "Nombre de Dios", "B??rt??rket"),
    (2020, 90, "Malta", "T??rket"),
    (2019, 50, "El Cherro", "T??rket");''') # ID = 1,2,3
    

    con.execute('''
    INSERT INTO FerdigBrentKaffe(Brenningsgrad, BrentDato, Beskrivelse, Kilopris, KaffeNavn, BrenneriNavn, KaffePartiID)
    VALUES
    ("Lysbrent", "20.01.2022", "En velsmakende og kompleks kaffe for m??rketiden", "600", "Vinterkaffe 2022", "Jacobsen og svart", "1"), 
    ("Morkbrent", "12.02.2022", "Floral med litt sjokoladesmak", "100", "Luksuskaffe", "Lang??ra Brenneri", "2"), 
    ("Mellombrent", "09.03.2022", "Ser lys ut men har mork smak", "60", "Bygdekaffe", "Hringariki", "3");''') # ID = 1,2,3

    con.execute(''' 
        INSERT INTO Bruker(BrukerEpost,BrukerPassord,Fornavn,Etternavn)
        VALUES
    ("eliasbsv@gmail.com", "helene123", "Elias", "Svin??"),
    ("thomas.frette@gmail.com", "helene123", "Thomas", "Frette"),
    ("helene.bjornsen@gmail.com", "helene123", "Helene", "Bjornsen"),
    ("katrine.bjune@gmail.com", "helene123", "Katrine", "Bjune"),
    ("marie.holmeide@gmail.com", "helene123", "Marie", "Holmeide"),
    ("sensor@gmail.com", "sensor","Sensor", "Sensor"); ''')

    con.execute('''
    INSERT INTO Kaffesmaking(Smaksnotater, Rangering, BrukerEpost, FerdigBrentKaffeID)
    VALUES
    ("Skikkelig digg liksom", 9, "eliasbsv@gmail.com", "1"),
    ("Veldig grei men litt for grov", 7, "thomas.frette@gmail.com", "2"),
    ("Likte den ikke litt engang", 2,  "helene.bjornsen@gmail.com", "3"); ''')

    con.execute('''
        INSERT INTO Dyrket (KaffeB??nneID,G??rdsNavn)
        VALUES 
            (1,"Nombre de dias"),
            (2,"Malta"),
            (3,"El Cherro");
    ''')

    con.execute('''
        INSERT INTO iKaffeParti (KaffePartiID,KaffeB??nneID)
        VALUES 
            (1,1),
            (2,2),
            (3,3);
    ''')

    con.commit()

createTables()

fillDummyData()


