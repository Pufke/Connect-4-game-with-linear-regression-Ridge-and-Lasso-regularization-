"""
Modul u kome su minmax, GUI.
"""
import math
import random
from .constant import *

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
    myimage = pygame.image.load("picture/numerika.png")
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