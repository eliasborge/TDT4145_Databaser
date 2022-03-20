import sqlite3

con = sqlite3.connect("KaffeDB.db")
cursorObj = con.cursor()

aktivBruker = 0


def lagBruker():
    print("Fyll inn feltene:")
    brukerEpost = input("\nEpost: ")
    brukerFornavn = input("\nFornavn: ")
    brukerEtternavn = input("\nEtternavn: ")
    brukerPassord = input("\nPassord: ")
    #Koble/registrere til databasen

    sql = "INSERT INTO Bruker (BrukerEpost, BrukerPassord, Fornavn, Etternavn) VALUES (?,?,?,?)"
    val = (brukerEpost,brukerPassord,brukerFornavn,brukerEtternavn)
    cursorObj.execute(sql,val)

    con.commit()
    print(cursorObj.rowcount, "record inserted")
    


lagBruker()

def login():
    print("Logg inn eller registrer deg")
    
    brukersvar = input("Trykk på B for å lage en bruker eller trykk på L for å logge inn")

    if(brukersvar == "B"):
        #Lag bruker
        lagBruker()
    else:
        print("Vennligst skriv inn epost og passord") 
        epost = input()  
        #registrer


def starter():
    int("Velkommen til KaffeDB")
    print("Meny: ")
    print("Trykk på K for å legge til en kaffesmaking")
    print("Trykk på S for å søke")
    print("Trykk på D for å slette en kaffesmaking")
    svar = input("Velg 1 alternativ: ")

    if(svar == "gdkdk"):
        søk()
    

def  kaffeSmaking():
    print("Ny kaffesmaking")
    rangering = input("\nRangering: ")
    smaksdato = input("\nSmaksdato: ")
    smaksnotater = input("\nSmaksnotat: ")
    
def søk():
    hei = 0
    #Navn
    #


def slett():
    slett = 0


