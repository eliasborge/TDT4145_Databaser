import sqlite3

con = sqlite3.connect("KaffeDB.db")



def lagBruker():
    print("Fyll inn feltene:")
    brukerEpost = input("\nEpost: ")
    brukerFornavn = input("\nFornavn: ")
    brukerEtternavn = input("\nEtternavn: ")
    brukerPassord = input("\nPassord: ")
    #Koble/registrere til databasen
    
    con.execute(''' 
        INSERT INTO Bruker(BrukerEpost,BrukerPassord,Fornavn,Etternavn)
        VALUES(%d,%d,%d,%d)
    ''',brukerEpost,brukerPassord,brukerFornavn,brukerEtternavn)
lagBruker()

def login():
    print("Logg inn eller registrer deg")
    
    brukersvar = input("Trykk på B for å lage en bruker eller trykk på L for å logge inn")

    if(brukersvar == "B"):
        #Lag bruker
        lagBruker()
    else:
        print()   
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
    rangering = input("\nRangering (0-10): ")
    smaksdato = input("\nSmaksdato: ")
    smaksnotater = input("\nSmaksnotat: ")

def click():
    hei = 0
    
def søk():
    hei = 1
    print("Her kan du filtrere den informasjonen du øsnker, eksempelvis på land, region eller bønnetype.")
    print("\nNavn")
    #Land (Ferdigbrent kaffe fra land X)
    print("\nLand")
    #Region (Ferdigbrent kaffe fra region X)
    print("\nRegion")
    #BonneType (Bonnetype inngaar i X ferdigbrent kaffer)
    print("\nBønnetype")
    #Brenneri (mest populeare)
    print("\nBrenneri")
    #Smaksnotat (maa kunne soke paa et ord eks. "floral". Brukeren skal få tilbake en liste med 
    #brennerinavn og kaffenavn.)
    print("\nSmaksnotat")
    if click == "Navn":
        # antall kaffesmakinger hen har
        hei = 0
    elif click == "Land":
        #Ferdigbrent kaffe fra land X
        hei = 0
    elif 





def slett():
    slett = 0


