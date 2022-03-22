import sqlite3

con = sqlite3.connect("KaffeDB.db")
cur = con.cursor()

activeUser = "-1"


def lagBruker():
    print("Fyll inn feltene:")
    brukerEpost = input("\nEpost: ")
    brukerFornavn = input("\nFornavn: ")
    brukerEtternavn = input("\nEtternavn: ")
    brukerPassord = input("\nPassord: ")
    # Koble/registrere til databasen

    con.execute(''' 
        INSERT INTO Bruker(BrukerEpost,BrukerPassord,Fornavn,Etternavn)
        VALUES(?,?,?,?)
    ''', (brukerEpost, brukerPassord, brukerFornavn, brukerEtternavn))

    con.commit()

    login()

# NICE TO HAVE MEN IKKE MUST FUNGERER NÅ.


def login():
    print("Logg inn eller registrer deg")

    brukersvar = input(
        "Trykk på B for å lage en bruker eller trykk på L for å logge inn \n")

    if(brukersvar.lower() == "b"):
        # Lag bruker
        lagBruker()
    else:
        print("Vennligst skriv inn E-post og passord.")
        epost = input("E-post: ")
        passord = input("Passord: ")

        cur.execute("SELECT BrukerEpost,BrukerPassord FROM Bruker")
        resultat = cur.fetchall()
        for element in resultat:
            if(element[0] == epost and element[1] == passord):
                activeUser = element[0]
                print("Login success")
                return True
        print("login failed. Try again")
        return False


def kaffeSmaking():
    print("Ny kaffesmaking")
    rangering = input("\nRangering (0-10): ")
    smaksdato = input("\nSmaksdato: ")
    smaksnotater = input("\nSmaksnotat: ")
    kaffenavn = input("Kaffenavn: ")
    brenneri = input("Brenneri: ")

    cur.execute(
        "SELECT FerdigBrentKaffeID, KaffeNavn, BrenneriNavn FROM FerdigBrentKaffe")
    results = cur.fetchall()
    for element in results:
        if(kaffenavn == element[1] and brenneri == element[2]):
            kaffe = element
            con.execute("INSERT INTO KaffeSmaking VALUES (?,?,?,?,?)",
                        (smaksnotater, rangering, smaksdato, activeUser, kaffe[0]))
            con.commit()
            print("\nKaffesmakingen er lagt til i ditt arkiv.")
            return
    print("Kaffen du skrev inn finnes ikke i systemene våre. \n Sjekk at du har skrevet inn korrekt informasjon")


def penger():
    print("Her er oversikten over kaffetypene som gir deg mest for pengene: \n")


def flestSmak():
    print("Her er oversikten over brukerne som har smakt flest kaffetyper: \n")
    cur.execute(''' 
    SELECT Fornavn, Etternavn, COUNT(DISTINCT KaffeSmakingID) AS antall
    FROM Bruker INNER JOIN KaffeSmaking KS on Bruker.BrukerEpost = KS.BrukerEpost
    GROUP BY(Fornavn,Etternavn)
    ORDER BY antall DESC

    ''')
    results = cur.fetchall()
    print("Fornavn        | Etternavn        | Antall ")
    for tuple in results:
        print(tuple[0]+" "*(17-len(tuple[0]))+tuple[1]+" "*(18-len(tuple[1])) + tuple[2])
    


def floral():
    print("Her er oversikten over florale kaffetyper: \n")
    cur.execute(''' 
    SELECT BrenneriNavn, KaffeNavn
    FROM FerdigBrentKaffe
    WHERE Beskrivelse LIKE '''+"%"+'''floral%'
    ''')
    results = cur.fetchall()
    print("Brennerinavn        | KaffeNavn")
    for tuple in results:
        print(tuple[0]+" "*(22-len(tuple[0]))+tuple[1])


def uvaskede():
    print("Her er oversikten over uvaskede kaffetyper fra Rwanda og Colombia: \n")


# MÅ ENDRE DENNE TODO
def meny():
    if(login()):
        print("Du er logget inn som: " + activeUser + "\n\n")
        print("Velkommen til KaffeDB")
        print("Meny: \n")
        print("Trykk på K for å legge til en kaffesmaking\n")
        print("Trykk på P for å se hvilken kaffe som gir deg mest for pengene\n")
        print("Trykk på B for å se hvilke brukere som har smakt flest typer kaffe\n")
        print("Trykk på F for å søke etter florale kaffetyper\n")
        print("Trykk på V for å søke etter kaffetyper fra Rwanda og Colombia som ikke er vaskede\n")
        svar = input("Velg 1 alternativ: ")

        if(svar.lower() == "k"):
            kaffeSmaking()
        elif(svar.lower() == "p"):
            penger()

        elif(svar.lower() == "b"):
            flestSmak()

        elif(svar.lower() == "f"):
            floral()

        elif(svar.lower() == "v"):
            uvaskede()



meny()