
def lagBruker():
    print("Fyll inn feltene:")
    brukerEpost = input("/n Epost: ")
    brukerFornavn = input("/n Fornavn: ")
    brukerEtternavn = input("/n Etternavn: ")
    brukerPassord = input("/n Passord: ")
    #Koble/registrere til databasen

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
    print("Velkommen til KaffeDB")
    print("Meny: ")
    print("Trykk på K for å legge til en kaffesmaking")
    print("Trykk på S for å søke")
    print("Trykk på D for å slette en kaffesmaking")

