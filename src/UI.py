from contextlib import nullcontext
import sqlite3

###############################################
#
# DATABASE PROSJEKT DEL 2
# VELKOMMEN TIL KaffeDB SITT GRENSESNITT
# 
#
###############################################

con = sqlite3.connect("KaffeDB.db")
cur = con.cursor()

isLoggedIn = False
# Innlogging for sensor
# Epost: sensor@gmail.com Passord: sensor


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

    meny()



#Innlogging
def login():
    global activeUser

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
                global isLoggedIn
                isLoggedIn = True
                print("Login success")
                return True

        print("login failed. Try again")
        meny()
        return False

#Metode for å smake kaffe
def kaffeSmaking():
    #Tar inn data fra bruker
    print("Ny kaffesmaking")
    rangering = input("\nRangering (0-10): ")
    smaksdato = input("\nSmaksdato (yyyy-mm-dd) - La den stå tom for dagens dato, trykk enter: ")
    smaksnotater = input("\nSmaksnotat: ")
    cur.execute(
        "SELECT KaffeNavn FROM FerdigBrentKaffe")

    results = cur.fetchall()
    print("KaffeNavn ")
    print("-"*10)
    counter = 0
    #Viser mulige kaffevalg
    for x, tuple in enumerate(results):
        print(str(x + 1) + " " + tuple[0])
        counter += 1
    
    valg = 0
    while (valg < 1 or valg > counter):
        valg = int(input("Velg mellom 1 til " + str(counter) + ": "))

    kaffenavn = results[valg-1][0]

    cur.execute(
        "SELECT BrenneriNavn FROM KaffeBrenneri"
    )
    #Viser mulige brennerivalg
    results = cur.fetchall()
    print("Brennerinavn ")
    print("-"*10)
    counter = 0
    for x, tuple in enumerate(results):
        print(str(x + 1) + " " + tuple[0])
        counter += 1

    valg = 0
    while (valg < 1 or valg > counter):
        valg = int(input("Velg mellom 1 til " + str(counter) + ": "))
    brenneri = results[valg - 1][0]

    cur.execute(
        "SELECT FerdigBrentKaffeID, KaffeNavn, BrenneriNavn FROM FerdigBrentKaffe")
    results = cur.fetchall()
    for element in results:
        print(element[1])
        if(kaffenavn == element[1] and brenneri == element[2]):
            #Her er det if/else for å skille mellom om brukeren vil bruke dagens dato eller en manuell input.
            if(smaksdato != ""):
                kaffe = element
                con.execute("INSERT INTO KaffeSmaking(SmaksNotater, Rangering, SmaksDato,BrukerEpost, FerdigBrentKaffeID) VALUES (?,?,?,?,?)",
                        (smaksnotater, rangering, smaksdato, activeUser, kaffe[0]))
                con.commit()
                print("\nKaffesmakingen er lagt til i ditt arkiv.")
                return
            else:
                kaffe = element
                con.execute("INSERT INTO KaffeSmaking(SmaksNotater, Rangering,BrukerEpost, FerdigBrentKaffeID) VALUES (?,?,?,?)",
                        (smaksnotater, rangering, activeUser, kaffe[0]))
                con.commit()
                print("\nKaffesmakingen er lagt til i ditt arkiv.")
                return
    print("Kaffen du skrev inn finnes ikke i systemene våre. \n Sjekk at du har skrevet inn korrekt informasjon")

#Metode for å printe hvilke kaffetyper som gir mest for pengene
def penger():
    print("Her er oversikten over kaffetypene som gir deg mest for pengene: \n")
    cur.execute('''
    SELECT BrenneriNavn, kaffeNavn, Kilopris, AVG(Rangering) AS gjennomsnitt
    FROM KaffeSmaking INNER JOIN FerdigBrentKaffe FBK on FBK.FerdigBrentKaffeID = KaffeSmaking.FerdigBrentKaffeID
    GROUP BY FBK.FerdigBrentKaffeID
    ORDER BY (gjennomsnitt) DESC
    ''')

    results = cur.fetchall()
    print("Brennerinavn        | KaffeNavn        | Pris   | Gjennomsnittsscore ")
    for tuple in results:
        print("-"*70)
        print(tuple[0]+" "*(22-len(tuple[0]))+tuple[1]+" "*(18-len(tuple[1])
                                                            ) + str(tuple[2])+" "*(10 - len(str(tuple[2]))) + str(tuple[3]))


# Hvilke brukere som har smakt flest typer kaffe.
def flestSmak():
    print("Her er oversikten over brukerne som har smakt flest kaffetyper: \n")
    cur.execute(''' 
    SELECT Fornavn, Etternavn, COUNT(DISTINCT KaffeSmakingID) AS antall
    FROM Bruker INNER JOIN KaffeSmaking KS on Bruker.BrukerEpost = KS.BrukerEpost
    GROUP BY Fornavn, Etternavn
    ORDER BY antall DESC;
    ''')
    results = cur.fetchall()
    print("Fornavn        | Etternavn        | Antall ")
    for tuple in results:
        print("-"*50)
        print(tuple[0]+" "*(17-len(tuple[0]))+tuple[1] +
              " "*(18-len(tuple[1])) + str(tuple[2]))


# Kaffer som er beskrevet som florale
def floral():
    print("Her er oversikten over florale kaffetyper: \n")
    cur.execute(''' 
    SELECT BrenneriNavn, KaffeNavn
    FROM FerdigBrentKaffe
    WHERE Beskrivelse LIKE +'%floral%';
    ''')
    results = cur.fetchall()
    print("Brennerinavn        | KaffeNavn")
    for tuple in results:
        print("-"*50)
        print(tuple[0]+" "*(22-len(tuple[0]))+tuple[1])
    print("\n")

#Kaffer som er uvaskede og fra Colombia eller Rwanda.
def uvaskede():
    print("Her er oversikten over uvaskede kaffetyper fra Rwanda og Colombia: \n")
    cur.execute('''
    SELECT FerdigBrentKaffe.BrenneriNavn, KaffeNavn
    FROM FerdigBrentKaffe INNER JOIN KaffeParti ON FerdigBrentKaffe.KaffePartiID = KaffeParti.KaffePartiID
    INNER JOIN Gård G on KaffeParti.GårdsNavn = G.GårdsNavn
    WHERE (G.Land LIKE 'Rwanda' OR G.Land LIKE 'Colombia') AND (KaffeParti.MetodeNavn NOT LIKE 'Vasket');
    ''')

    results = cur.fetchall()
    print("Brennerinavn       | Kaffenavn")
    for tuple in results:
        print("-"*50)
        print(tuple[0] + " "*(22-len(tuple[0])) + tuple[1])


# Main metode. Printer menyen og tar inn inputs fra bruker.
def meny():

    if(isLoggedIn or login()):
        print("\n\nDu er logget inn som: " + activeUser + "\n\n")
        print("Velkommen til KaffeDB")
        print("Trykk enter for å avslutte")
        print("Meny: \n")
        print("Trykk på K for å legge til en kaffesmaking\n")
        print("Trykk på P for å se hvilken kaffe som gir deg mest for pengene\n")
        print("Trykk på B for å se hvilke brukere som har smakt flest typer kaffe\n")
        print("Trykk på F for å søke etter florale kaffetyper\n")
        print("Trykk på V for å søke etter kaffetyper fra Rwanda og Colombia som ikke er vaskede\n")
        svar = input("Velg 1 alternativ: ")

        if(svar.lower() == "k"):
            kaffeSmaking()
            meny()
        elif(svar.lower() == "p"):
            penger()
            meny()

        elif(svar.lower() == "b"):
            flestSmak()
            meny()

        elif(svar.lower() == "f"):
            floral()
            meny()

        elif(svar.lower() == "v"):
            uvaskede()
            meny()
        else:
            return

#Kjører appen
meny()
