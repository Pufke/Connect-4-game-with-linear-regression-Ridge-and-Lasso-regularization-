import numpy as np 
import pygame 
import sys
import math
import random
import ctypes
import imageio
import csv
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.rcParams.update({'font.size': 12})
from sklearn.datasets import load_boston
#from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
import ctypes


PLAYER = 0
AI = 1
PRAZNO_POLJE = 0
PLAYER_TOKEN = 1
AI_TOKEN = 2

BROJ_REDOVA = 6
BROJ_KOLONA = 6
POVRSINA_ZA_POBEDU = 4

BELA = (255,255,255)
SIVA = (200,200,200)
TAMNO_SIVA = (117, 117, 117)
CRNA = (0,0,0)
ZUTA = (255,255,0)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

pom_y = []
#F-ja koja kreira matricu 6 puta 6, koja predstavlja tablu
def kreiraj_tablu():
    tabla = np.zeros((BROJ_REDOVA,BROJ_KOLONA))
    return tabla

#F-ja koja okrece nasu tablu, jer je u numpy biblioteci kord pocetak, u gonjem levom cosku
def stampaj_tablu(tabla):
    print(np.flip(tabla,0))

#F-ja koja postavlja token na odgovarajucu poziciju u matrici
def postavi_token(tabla,red,kolona,token):
    tabla[red][kolona] = token

#F-ja koja provera da li je validna lokacija, tj da li je 5 red prosledjene kolone slobodan
def da_li_je_popunjena_kolona(tabla, kolona):
    return tabla[BROJ_REDOVA-1][kolona] == 0

#F-ja koja vraca indeks prvog slobodnog reda
def get_sledeci_slobodan_red(tabla,kolona):
    for i in range(BROJ_REDOVA):
        if tabla[i][kolona] == 0:
            return i

#F-ja koja odredjuje da li je odigrani potez pobednicki
def winning_move(tabla,token):
    # proveri horizontalne lokacije
    for c in range(BROJ_KOLONA-3):
        for r in range(BROJ_REDOVA):
            if tabla[r][c] == token and tabla[r][c+1] == token and tabla[r][c+2] == token and tabla[r][c+3] == token:
                return True

    # proveri vertikalne lokacije
    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA-3):
            if tabla[r][c] == token and tabla[r+1][c] == token and tabla[r+2][c] == token and tabla[r+3][c] == token:
                return True

    # proveri lokacije na glavnoj dijagonali 
    for c in range(BROJ_KOLONA-3):
        for r in range(BROJ_REDOVA-3):
            if tabla[r][c] == token and tabla[r+1][c+1] == token and tabla[r+2][c+2] == token and tabla[r+3][c+3] == token:
                return True

    #proveri lokacije na sporednoj dijagonali
    for c in range(BROJ_KOLONA-3):
        for r in range(3, BROJ_REDOVA):
            if tabla[r][c] == token and tabla[r-1][c+1] == token and tabla[r-2][c+2] == token and tabla[r-3][c+3] == token:
                return True

#F-ja koja vrsi renderovanje GUI-a tj prikaz nase igre
def iscrtaj_tablu(tabla):
    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA):
            pygame.draw.rect(screen, BELA, (c*VELICINA_KVADRATA, r*VELICINA_KVADRATA+VELICINA_KVADRATA, VELICINA_KVADRATA, VELICINA_KVADRATA))
            pygame.draw.circle(screen, SIVA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), int(r*VELICINA_KVADRATA+VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)
    
    for c in range(BROJ_KOLONA):
        for r in range(BROJ_REDOVA):        
            if tabla[r][c] == PLAYER_TOKEN:
                pygame.draw.circle(screen, ZUTA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), height - int(r*VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)
            elif tabla[r][c] == AI_TOKEN:
                pygame.draw.circle(screen, CRNA, (int(c*VELICINA_KVADRATA+VELICINA_KVADRATA/2), height - int(r*VELICINA_KVADRATA+VELICINA_KVADRATA/2)), RADIUS)


    pygame.draw.rect(screen, BELA, (200,630, 500, 500))
    #Ucitavamo sliku
    myimage = pygame.image.load("numerika.png")
    screen.blit(myimage, (0, 630)) #Parametri blit-a su slika, (xPozicija,yPozicija)
                                     #Blit je termin koji se koristi za renderovanje



    pygame.display.update()


#F-ja koja daje bodove celijama nase tabele
def proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token):
    score = 0
    protivnicki_token = PLAYER_TOKEN
    if token == PLAYER_TOKEN:
        protivnicki_token = AI_TOKEN

    if povrsina_za_pobedu.count(token) == 4:
        score += 100
    elif povrsina_za_pobedu.count(token) == 3 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 1:
        score += 5
    elif povrsina_za_pobedu.count(token) == 2 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 2:
        score += 2

    if povrsina_za_pobedu.count(protivnicki_token) == 3 and povrsina_za_pobedu.count(PRAZNO_POLJE) == 1:
        score -= 40

    return score

#F-ja koja vrsi bodovanje 
def score_position(tabla, token):
    score = 0

    ## Boduj centralnu kolonu
    center_array = [int(i) for i in list(tabla[:, BROJ_KOLONA//2])]
    centaralni_brojac = center_array.count(token)
    score += centaralni_brojac * 3

    ## Boduj horizontalno
    for r in range(BROJ_REDOVA):
        red_array = [int(i) for i in list(tabla[r,:])]
        for c in range(BROJ_KOLONA-3):
            povrsina_za_pobedu = red_array[c:c+POVRSINA_ZA_POBEDU]
            score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

    ## Boduj vertikalno u pozitivno smeru(na gore)
    for c in range(BROJ_KOLONA):
        kolona_array = [int(i) for i in list(tabla[:,c])]
        for r in range(BROJ_REDOVA-3):
            povrsina_za_pobedu = kolona_array[r:r+POVRSINA_ZA_POBEDU]
            score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

    ## Boduj vertiaklno u negativnom smeru(na dole)
    for r in range(BROJ_REDOVA-3):
        for c in range(BROJ_KOLONA-3):
            povrsina_za_pobedu = [tabla[r+i][c+i] for i in range(POVRSINA_ZA_POBEDU)]
            score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

    for r in range(BROJ_REDOVA-3):
        for c in range(BROJ_KOLONA-3):
            povrsina_za_pobedu = [tabla[r+3-i][c+i] for i in range(POVRSINA_ZA_POBEDU)]
            score += proceni_povrsinu_za_pobedu(povrsina_za_pobedu, token)

    return score

#F-ja koja trazi sve validne(prazne) lokacije i smesta ih u niz,
# npr ako ako ni jedna kolona nije popunjena niz izgleda valid_location = [0,1,2,3,4,5]
def get_validne_lokacije(tabla):
    validne_lokacije = []
    for kolona in range(BROJ_KOLONA):
        if da_li_je_popunjena_kolona(tabla, kolona):
            validne_lokacije.append(kolona)
    return validne_lokacije

# F-ja koja vraca najpogodniju kolonu za odigrati potez
def izaberi_najbolji_potez(tabla, token):

    validne_lokacije = get_validne_lokacije(tabla)
    best_score = -10000
    best_kolona = random.choice(validne_lokacije)
    for kolona in validne_lokacije:
        red = get_sledeci_slobodan_red(tabla, kolona)
        temp_tabla = tabla.copy()
        postavi_token(temp_tabla, red, kolona, token)
        score = score_position(temp_tabla, token)
        if score > best_score:
            best_score = score
            best_kolona = kolona

    return best_kolona

def is_terminal_node(tabla):
    return winning_move(tabla, PLAYER_TOKEN) or winning_move(tabla, AI_TOKEN) or len(get_validne_lokacije(tabla)) == 0

def minimax(tabla, depth, alpha, beta, maximizingPlayer):
    validne_lokacije = get_validne_lokacije(tabla)
    is_terminal = is_terminal_node(tabla)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(tabla, AI_TOKEN):
                return (None, 100000000000000)
            elif winning_move(tabla, PLAYER_TOKEN):
                return (None, -10000000000000)
            else: # Kraj igre, zato sto nema vise validnih poteza
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(tabla, AI_TOKEN))
    if maximizingPlayer:
        value = -math.inf
        kolonaumn = random.choice(validne_lokacije)
        for kolona in validne_lokacije:
            red = get_sledeci_slobodan_red(tabla, kolona)
            b_copy = tabla.copy()
            postavi_token(b_copy, red, kolona, AI_TOKEN)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                kolonaumn = kolona
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return kolonaumn, value

    else: # Minimizing player
        value = math.inf
        kolonaumn = random.choice(validne_lokacije)
        for kolona in validne_lokacije:
            red = get_sledeci_slobodan_red(tabla, kolona)
            b_copy = tabla.copy()
            postavi_token(b_copy, red, kolona, PLAYER_TOKEN)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                kolonaumn = kolona
            beta = min(beta, value)
            if alpha >= beta:
                break

        return kolonaumn, value

def lasso_regression(data, predictors, alpha, models_to_plot={}):
    #Fit the model
    lassoreg = Lasso(alpha=alpha,normalize=True, max_iter=1e5)
    lassoreg.fit(data[predictors],data['y'])
    y_pred = lassoreg.predict(data[predictors])
    print("Predikcija poteza", y_pred)
  
    
    #Return the result in pre-defined format
    rss = sum((y_pred-data['y'])**2)
    ret = [rss]
    ret.extend([lassoreg.intercept_])
    ret.extend(lassoreg.coef_)
    return ret

def ridge_regression(data, predictors, alpha):

    #Fit the model
    ridgereg = Ridge(alpha=alpha,normalize=True)
    ridgereg.fit(data[predictors],data['y'])
    y_pred = ridgereg.predict(data[predictors])
    print("Predikcija poteza", y_pred)
    print("PREDIKCIJA ZA PRVI POTEZ", y_pred[1])
   
    for p in y_pred:
        if p not in pom_y:
            pom_y.append(p)
    
    for x in range(len(pom_y)):
        print("Predikcija za potez ", x+1 , round(abs(pom_y[x])))


    #Return the result in pre-defined format
    rss = sum((y_pred-data['y'])**2)
    ret = [rss]
    ret.extend([ridgereg.intercept_])
    ret.extend(ridgereg.coef_)
    return ret

class DynamicArray(object): 
    ''' 
    DYNAMIC ARRAY CLASS (Similar to Python List) 
    '''
    def __init__(self): 
        self.n = 0 # Count actual elements (Default is 0) 
        self.capacity = 1 # Default Capacity 
        self.A = self.make_array(self.capacity) 
          
    def __len__(self): 
        """ 
        Return number of elements sorted in array 
        """
        return self.n 
      
    def __getitem__(self, k): 
        """ 
        Return element at index k 
        """
        if not 0 <= k <self.n: 
            # Check it k index is in bounds of array 
            return IndexError('K is out of bounds !')  
          
        return self.A[k] # Retrieve from the array at index k 
          
    def append(self, ele): 
        """ 
        Add element to end of the array 
        """
        if self.n == self.capacity: 
            # Double capacity if not enough room 
            self._resize(2 * self.capacity)  
          
        self.A[self.n] = ele # Set self.n index to element 
        self.n += 1
          
    def _resize(self, new_cap): 
        """ 
        Resize internal array to capacity new_cap 
        """
          
        B = self.make_array(new_cap) # New bigger array 
          
        for k in range(self.n): # Reference all existing values 
            B[k] = self.A[k] 
              
        self.A = B # Call A the new bigger array 
        self.capacity = new_cap # Reset the capacity 
          
    def make_array(self, new_cap): 
        """ 
        Returns a new array with new_cap capacity 
        """
        return (new_cap * ctypes.py_object)() 

tabla = kreiraj_tablu()
game_over = False

# Konfigurisanje GUI-a
pygame.init()
VELICINA_KVADRATA = 90
PROSTOR_ZA_SLIKU = 240
width = BROJ_KOLONA * VELICINA_KVADRATA
height = (BROJ_REDOVA+1) * VELICINA_KVADRATA 
size = (width, height+ PROSTOR_ZA_SLIKU)
RADIUS = int(VELICINA_KVADRATA/2 - 5)
screen = pygame.display.set_mode(size)

iscrtaj_tablu(tabla)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 55)
fontZaButtn = pygame.font.SysFont("monospace", 20)

turn = random.randint(PLAYER, AI)

indikator = -1
if turn == PLAYER:
    indikator = 1

# Inijalizacija dinamickog niza
nizPoteza = DynamicArray() 

# Dve liste koje sluze iscitavanje trainingSet kako bi vrsil numericke proracune nad njima
x = []
y = []

# Iscitavanje iz fajla i smestanje u liste x i y
with open('trainingSet.csv', 'r') as csvfile:
    citac = csv.reader(csvfile, delimiter='\t')
    next(citac)
    for entitet in citac:
        x.append(int(entitet[0]))
        y.append(int(entitet[1]))

# Ispisivanje ucitanih lista
print(x)
print(y)
while not game_over:

    # Prolazak kroz Event Lisenere od koristi i njihova implementacija
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BELA, (0,0, width, VELICINA_KVADRATA))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, ZUTA, (posx, int(VELICINA_KVADRATA/2)), RADIUS)
                
            mouse = pygame.mouse.get_pos()
            #print(mouse)
            if 300+100 > mouse[0] > 300 and 650+50 > mouse[1] > 650:
                pygame.draw.rect(screen, TAMNO_SIVA,(300,650,160,50))
            else:
                pygame.draw.rect(screen, SIVA,(300,650,160,50))    

            label1 = fontZaButtn.render("Pomoc", 1, CRNA)
            label2 = fontZaButtn.render("numerike", 1, CRNA)
            screen.blit(label1, (348,655)) #Prvi parametar x pozicija texta, drugi parametar y pozicija
            screen.blit(label2, (333,675))
        
          
            
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BELA, (0,0, width, VELICINA_KVADRATA))

            if 300+100 > mouse[0] > 300 and 650+50 > mouse[1] > 650:     

                #Define input array with angles from 60deg to 300deg converted to radians
                #x = [1, 1,2 ,2,3,3,3,4,4,4,5,5,6,6,7,7,7,7,8,8,8,8,9,9,9,10,10,10,10,11,11,11,11,12,12,12,12,13,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
                np.random.seed(10)  #Setting seed for reproducability
                #y = 4.5 + np.random.normal(0,1,len(x))
                data = pd.DataFrame(np.column_stack([x,y]),columns=['x','y'])
                for i in range(2,16):  #power of 1 is already there
                    colname = 'x_%d'%i      #new var will be x_power
                    data[colname] = data['x']**i

                #Initialize predictors to be set of 15 powers of x
                predictors=['x']
                predictors.extend(['x_%d'%i for i in range(2,16)])

                #Set the different values of alpha to be tested
                #alpha_ridge = [1e-15, 1e-10, 1e-8, 1e-4, 1e-3,1e-2, 1, 5, 10, 20]
                alpha_ridge = [1e-4]

                #Initialize the dataframe for storing coefficients.
                col = ['rss','intercept'] + ['coef_x_%d'%i for i in range(1,16)]
                ind = ['alpha_%.2g'%alpha_ridge[0]]
                coef_matrix_ridge = pd.DataFrame(index=ind, columns=col)

                models_to_plot = {1e-4:233}  
        
                coef_matrix_ridge.iloc[0,] = ridge_regression(data, predictors, alpha_ridge[0])

                if indikator==-1:
                    ctypes.windll.user32.MessageBoxW(0, "Pomoc"+ " numerike : U vasem potezu " + str(len(nizPoteza)) + " odigraj " + str(int(round(pom_y[len(nizPoteza)]))), "Predlog poteza", 1)
                else:
                    ctypes.windll.user32.MessageBoxW(0, "Pomoc"+ " numerike : U vasem potezu " + str(len(nizPoteza)+1) + " odigraj " + str(int(round(pom_y[len(nizPoteza)+1]))), "Predlog poteza", 1)
                
            
            if turn == PLAYER:

                if mouse[1] < 620:
                    # normalizujemo poziciju, tj kako bi na osnovu piksela 641,dobili da je to 6 kolona recimo.
                    posx = event.pos[0]
                    kolona = int(math.floor(posx/VELICINA_KVADRATA)) 

                    if da_li_je_popunjena_kolona(tabla,kolona):
                        red = get_sledeci_slobodan_red(tabla,kolona)
                        postavi_token(tabla,red,kolona,PLAYER_TOKEN)

                        if winning_move(tabla,PLAYER_TOKEN):
                            label = myfont.render("POBEDA ZUTOG !!", 1, ZUTA)
                            screen.blit(label, (10,5))
                            game_over = True

                        stampaj_tablu(tabla)
                        iscrtaj_tablu(tabla)
                        # prelazak na sledeceg igraca
                        turn += 1
                        turn = turn % 2

    if turn == AI and not game_over:    
        #kolona = random.randint(0,BROJ_KOLONA-1)
        #kolona = izaberi_najbolji_potez(tabla,AI_TOKEN)
        # Podesavanjem depth-a , tj drugog parametra uticemo na tezinu igre
        kolona, minimax_score = minimax(tabla, 4, -math.inf, math.inf, True)

        if da_li_je_popunjena_kolona(tabla,kolona):
            red = get_sledeci_slobodan_red(tabla,kolona)
            postavi_token(tabla,red,kolona,AI_TOKEN)
        
            # Promenljive koje su nam potrebne za cuvanje u traningSetu
            brojPoteza=0
            brojKolone=0
            # Appendovanje novog elemnta, tj kolone koja je odigrana  
            nizPoteza.append(kolona) 
            for i in range(len(nizPoteza)):
                print("Broj poteza" ,i+1, " AI je odigrao na kolonu ", nizPoteza[i] )
                brojPoteza=i
                brojKolone=nizPoteza[i]

            # Prikupljanje podataka prilikom treniranja igre.
            with open('trainingSet.csv', 'a', newline='') as csvfile:
                imenaPolja = ['brojPoteza', 'brojKolone']
                writer = csv.DictWriter(csvfile, fieldnames=imenaPolja, delimiter='\t')
                writer.writerow({'brojPoteza': brojPoteza+1, 'brojKolone': brojKolone})

            if winning_move(tabla,AI_TOKEN):
                label = myfont.render("POBEDA CRNOG !!", 1, CRNA)
                screen.blit(label, (10,5))
                game_over = True

            stampaj_tablu(tabla)
            iscrtaj_tablu(tabla)
            # prelazak na sledeceg igraca
            turn += 1
            turn = turn % 2

    # Iskljucivanje igre nakon game_overa-a
    if game_over:
        pygame.time.wait(3000)

        # Ako zelimo da resetujemo nas trainingSet, zakomentarisemo deo gde se podaci pune
        # i otkomentarisemo ovo kako bi napravili prazan fajl ( odnosno resetovali traningSet)
        # NIJE PREPORUCLJIBO OVO RADITI !!!

        # with open('trainingSet.csv', 'w', newline='') as csvfile:
        #    imenaPolja = ['brojPoteza', 'brojKolone']
        #    writer = csv.DictWriter(csvfile, fieldnames=imenaPolja, delimiter='\t')

        #    writer.writeheader()


        
            