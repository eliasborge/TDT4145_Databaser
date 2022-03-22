import sqlite3


con = sqlite3.connect("KaffeDB.db")
cur = con.cursor()

activeUser = ""

def lagBruker():
    print("Fyll inn feltene:")
    brukerEpost = input("\nEpost: ")
    brukerFornavn = input("\nFornavn: ")
    brukerEtternavn = input("\nEtternavn: ")
    brukerPassord = input("\nPassord: ")
    #Koble/registrere til databasen
    
    con.execute(''' 
        INSERT INTO Bruker(BrukerEpost,BrukerPassord,Fornavn,Etternavn)
        VALUES(?,?,?,?)
    ''',(brukerEpost,brukerPassord,brukerFornavn,brukerEtternavn))

    login()
#NICE TO HAVE MEN IKKE MUST FUNGERER NÅ.
def login():
    print("Logg inn eller registrer deg")
    
    brukersvar = input("Trykk på B for å lage en bruker eller trykk på L for å logge inn \n")

    if(brukersvar.lower() == "b"):
        #Lag bruker
        lagBruker()
    else:
        print("Vennligst skriv inn E-post og passord.")
        epost = input("E-post: ")
        passord = input("Passord: ")

        cur.execute("SELECT BrukerEpost,BrukerPassord FROM Bruker")
        resultat = cur.fetchall()
        for element in resultat:
            if(element[0] == epost and element[1] == passord):
                activeUser = epost
                print("Login success")
                return
        print("login failed. Try again")
        login()

            
login()

#MÅ ENDRE DENNE TODO
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
    kaffenavn = input("Kaffenavn: ")
    brenneri = input("Brenneri: ")

    cur.execute("SELECT FerdigBrentKaffeID, KaffeNavn, BrenneriNavn FROM FerdigBrentKaffe")
    results = cur.fetchall()
    for element in results:
        if(kaffenavn == element[1] and brenneri == element[2]):
            kaffe = element
            con.execute("INSERT INTO KaffeSmaking VALUES (?,?,?,?,?)",
            (smaksnotater,rangering,smaksdato,activeUser,kaffe[0]))
            print("\nKaffesmakingen er lagt til i ditt arkiv.")
            return
    print("Kaffen du skrev inn finnes ikke i systemene våre. \n Sjekk at du har skrevet inn korrekt informasjon")


    #REVUDERE DENNE TODO
def søk():
    hei = 1
    print("Her kan du filtrere den informasjonen du øsnker, eksempelvis på land, region eller bønnetype.")
    print("Filter: ")
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
    filtrering = input("")




#TRENGER IKKE TODO
def slett():
    slett = 0


