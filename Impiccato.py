
# MODIFICARE DENTRO LA CLASSE Dizionario L'INDIZZO (self.indirizzo_file) DEL FILE CHE CONTIENE LE PAROLE
# E INSERIRE IL VOSTRO OPPURE METTERE QUESTO FILE NELLA STESSA CARTELLA DELL'FILE PAROLE COSI DA NON OCCORRE
# MODIFICARE TALE INDIRIZZO
#  
"""****************************************************************************
Gioco dell'impiccato sia in modalità giocatore singolo, sia in modatilà multipla
con la possibilità di sfidarsi a chi trova + parole o ad immetere noi le parole

****************************************************************************"""
#   Libreria per l'estrazione casuale di un numero intero
import time
from random import randint
import os

#   Per una mia comodità utilizziamo l'approccio di programmazione ad oggetti
class Dizionario ():
    #   Metodo costruttore
    def __init__(self):
        #   Numero linee nel file dal quale estrarre le parole
        # DA INSERIRE L'INDIZZO DEL FILE CHE CONTIENE LE PAROLE
        self.indirizzo_file = "Parole.txt"
        self.n_linee = 0
        #   Apriamo il file in modalità lettura 
        #   with -> Si occupa della chiusura del file di testo
        with open(self.indirizzo_file, 'r') as f:
            #   Appendiamo alla stringa line la linea estratta dal file di testo
            line = f.readline()
            #   Ripetimo la proceduta
            while True:
                #   Aggiungiamo una linea
                self.n_linee += 1
                #   Appendiamo alla stringa line la linea estratta dal file di testo
                line = f.readline()
                #   Verifichiamo che la linea non sia vuota, se essa e vuota vuol dire che il file di testo
                #   e stato visto tutto e quindi sappiamo da quante linee e formato
                if not line:
                    #   Usciamo dal while
                    break

    #   Sorteggiamo una parola tra quelle del dizzionario
    def sorteggio_parola(self):
        #   Variabile che conterrà la parola soteggiata
        parola = ''
        #   Sorteggiamo un numero che va da 0 al numero di linee nel file (-1 xke il conto inizia da 0)
        n = randint(0, self.n_linee-1)
        #   Apriamo il file in modalità lettura 
        #   with -> Si occupa della chiusura del file di testo
        with open(self.indirizzo_file, 'r') as f:
            #   Qui usiamo una funzione speciale sui file di testo ENUMERATE che lavora su una coppia di valori
            #   1 il numero di riga e 2 la riga quindi qui sapendo la righa nella quale abbiamo la parola
            for (i, line) in enumerate(f):
                #   Tramite if identifichiamo la parola e la salviamo
                if (i == n):
                    parola = line.strip() # Togliamo eventuali spazio di troppo
                    parola=parola.upper() # Rendiamo la parola tutta maiuscola per evitare incompressioni
                    #   Usciamo dal while
                    break
        return parola

#   Classe relativa al gioco
class Impiccato ():
    #   Metodo costruttore
    def __init__(self):
        #   Creiamo un oggetto che fa riferimento al dizionario
        self.diz = Dizionario()
        self.parola = ''
        self.lettere_indovinate = []
        self.lettere_dette = []
        self.vite = 6
        self.errori = 0
        self.omino = ("  O  ", " /|  "," /|\ ", "  |  ", " /   ", " / \ ")

    #   Giocatore singolo
    def singolo(self, parola):
        #   Creiamo un oggetto che fa riferimento al dizionario
        #   Sorteggiamo la parola dal dizionario
        self.parola=parola 
        self.parola= self.parola.upper()
        prima=False
        seconda=False
        #   Ripetiamo il tutto fin quando non troviamo la parola o terminiamo le vite
        while True:
            #   Mostriamo la parola mascherata, visto che la funzione ci restituisce 2 risultati li salviamo in una tupla
            (s, i) = self.maschera_parola() 

            print(s)

            if  i == len(self.parola):
                print("")
                print ("COMPLIMENTI HAI INDOVINATO")
                self.lettere_indovinate=[]
                self.lettere_dette= []
                self.errori=0
                return 1

            ch = input("Dammi una lettara -> ")
            ch = ch.upper()
         
            # Altrimenti verifichiamo se è presente nelle lettere dette o indovinate
            if (ch in self.lettere_indovinate):
                print ("Lettera gia detta riprova")
                time.sleep(1)
                continue
            
            elif (ch in self.lettere_dette):
                #   se è presente diamo un altra possibilià
                print ("Lettera gia detta riprova")
                time.sleep(1)
                continue
            
            #    Se il carattere in esame è presente nella parola
            elif ch in self.parola:
                #    Lo aggiungiamo alla lista delle lettere dette
                self.lettere_indovinate.append(ch)
            
            else:
                #   Altrimenti togliamo una vita
                self.errori +=1
                self.lettere_dette.append(ch)
                print ("Errore !")
                for i in range (self.errori) :
                    #print (f"i={i}")
                    if (i==1):
                        if prima:
                            continue
                        prima=True 
                    if (i==4):
                        if seconda:
                            continue
                        seconda=True
                    
                    print (self.omino[i]) 
                time.sleep(1)             

            # Se ho terminato le vite esco
            if (self.errori == self.vite):
                print("")
                print (f"Hai perso la parola è: {self.parola}")
                self.lettere_indovinate=[]
                self.lettere_dette= []
                self.errori=0
                prima=False
                seconda=False
                return 0

    #   Giocatore multiplo con parola a caso           
    def multiplo (self, giocatori, giri):
        giocatori=giocatori
        giri=giri
        punti_giocatori=[]
        for i in range (0, giocatori):
            punti_giocatori.append(0)

        # Controlliamo di esegure almeno un giro a giocatore
        modulo= giri%giocatori
        while ( modulo != 0 ):
            giri += 1
            modulo = giri%giocatori

        print(f"Dovete eseguire {giri}, per terminare la partita e scoprire chi vince")

        print('BUON DIVERTIMENTO')
        diz= Dizionario()
        giocatore=1

        for i in range (0, giri):
            print ('')
            print(f"Giro n°{i}")
            print (f"Tocca al giocatore {giocatore}")
            g=self.singolo(diz.sorteggio_parola())
            if (g==1):
                punti_giocatori[giocatore-1] +=1
            elif (g==0):
                if (punti_giocatori[giocatore-1] == 0 ):
                   punti_giocatori[giocatore-1] = 0 
                else: 
                    punti_giocatori[giocatore-1] -=1
            
            print (f" Hai fatto {punti_giocatori[giocatore-1]} punti")
            giocatore +=1
            if (giocatore > giocatori):
                giocatore=1
        
        max_punti=0
        max=""

        for i in range (0, giocatori):
            a=i+1
            if (punti_giocatori[i]>max_punti): 
                max_punti = punti_giocatori[i]
                max= " "
                max=str(a)
            elif (punti_giocatori[i] == max_punti):
                max = max + " / " + str(a)

        print ("")
        print (f"Ha vinto il giocatore {max} con {max_punti} punti")
        print ("")

    #   Giocatore multiplo con parola a scelta del giocatore
    def multiplo_parola (self, giocatori, giri):
        giocatori = giocatori
        giri = giri
        # Controlliamo di esegure almeno un giro a giocatore
        modulo = giri%giocatori
        while ( modulo != 0 ):
            giri += 1
            modulo = giri%giocatori

        punti_giocatori=[]
        for i in range (0, giocatori):
            punti_giocatori.append(0)
        
        print (" Siamo pronti, INIZIAMO!!!!!!")

        turno=0
        giocatore=0
        while True:
            turno += 1
            print (f"turno n {turno}")
            print (f"Giocatore {giocatori-giocatore} inserisci la paralo da indovinare:")
            parola= input("->")
            self.clearScreen()
            giocatore += 1
            print (f"E' il turno del giocatore {giocatore}")

            g=self.singolo(parola)
            if (g==1):
                punti_giocatori[giocatore-1] +=1
            elif (g==0):
                if (punti_giocatori[giocatore-1] == 0 ):
                   punti_giocatori[giocatore-1] = 0 
                else: 
                    punti_giocatori[giocatore-1] -=1

            print ("")
            print (f"Giocatore {giocatore} hai fatto {punti_giocatori[giocatore-1]} punti")

            if (giocatore == giocatori):
                giocatore=0

            if (turno==giri):
                break

        max_punti=0
        max=""

        for i in range (0, giocatori):
            a=i+1
            if (punti_giocatori[i]>max_punti): 
                max_punti = punti_giocatori[i]
                max= " "
                max=str(a)
            elif (punti_giocatori[i] == max_punti):
                max = max + " / " + str(a)
        print ("")
        print (f"Ha vinto il giocatore {max} con {max_punti} punti")
        print ("")

    def clearScreen(self):
        os.system("cls")

    def maschera_parola(self):
        stringa = ''
        i = 0
        vocali = ['A', 'E', 'I', 'O', 'U']
        #   Scorriamo la parola per mascherarla
        for c in self.parola:
            #    Se il carattere in esame non è presente nella lista lettere indovinate 
            if c not in self.lettere_indovinate:
                #   Verifico se esso non e una vocale
                if c not in vocali:
                    stringa += '_ '
                else:
                    stringa += '+ '
            else:
                # se il carattere e presente nella lista allora lo rendo visibile
                stringa += c + ' '
                i += 1

        return stringa, i
        
def main():
    print (""" BENVENUTI!
In questo mini gioco da terminale potrete giocare al famoso gioco dell'impiccato.
Potrete giocare in modalità singola o multipla. Inoltre in modalità multipla potrete scegliere
se sorteggiare a caso le parole da una vasta lista, contenute in un file di testo
dove potete aggiungerne sempre più oppure scegliere voi le parole.

Bando alle chiacchiere iniziamo \n""")
    #   Creiamo un oggetto che fa riferimento al gioco
    imp=Impiccato()
    while True:
        print("""Modalità di gioco:
Giocatore singolo, digitare S; 
Giocatore multiplo, digitare M;
Esci, digitare E;""")
        scelta= input("Scegli la tua modalità di gioco-> ")
        print ("")
        scelta=scelta.upper()

        if (scelta== "S"):
            #   Creiamo un oggetto che fa riferimento al dizionario 
            diz = Dizionario()
            imp.singolo(diz.sorteggio_parola())
            
        elif (scelta == "M"):
            scelta= input("""Vuoi giocare in modalità:
Parola casuale, digita C;
Parola scelta da voi, digita V;
->  """)
            scelta=scelta.upper()
            if (scelta== "C"):
                giocatori= input ("""NB. Bisogna essere almeno in 2 per giocare in questa modalità 
Quanti giocatori siete??? ->""")
                giocatori=int(giocatori)
                if (giocatori<2):
                    print ("Siete in pochi giocatori, scegli un'altra modalità")
                    continue
                giri= input ("Quanti turni volete fare?? -> ")
                giri= int (giri)
                c=imp.multiplo(giocatori, giri)
            if (scelta== "V"):
                giocatori= input ("""NB. Bisogna essere almeno in 2 per giocare in questa modalità 
Quanti giocatori siete??? ->""")
                giocatori=int(giocatori)
                if (giocatori<2):
                    print ("Siete in pochi giocatori, scegli un'altra modalità")
                    continue
                giri= input ("Quanti giri volete fare?? -> ")
                giri= int (giri)
                c=imp.multiplo_parola(giocatori, giri)

        else:
            break

        time.sleep(1.5)



#   Verifichiamo se il gioco viene lanciato 
if __name__ == '__main__':
    main()
