import pygame

def dessine_plateau():
    """
    Dessine le damier et place les pions si présents.
    """
    for i in range(nb_colonnes):
        for a in range(nb_lignes):
            x = marge_gauche + i * case_size
            y = marge_haut + a * case_size
            couleur = cases_blanches if (i + a) % 2 == 0 else cases_noires
            pygame.draw.rect(screen, couleur, (x, y, case_size, case_size))

            # Dessiner les pions
            if plateau[a][i] == 1:  # Pion blanc
                screen.blit(pion_noir, (x, y))
            elif plateau[a][i] == 2:  # Pion noir
                screen.blit(pion_blanc, (x, y))


def place_pions():
    """
    Place les pions sur les trois premières et trois dernières lignes.
    - Trois premières lignes : pions blancs sur cases noires.
    - Trois dernières lignes : pions noirs sur cases noires.
    """
    for a in range(4):  # Les trois premières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 != 0:  # Cases noires
                plateau[a][i] = 1  # Pions blancs

    for a in range(nb_lignes - 4, nb_lignes):  # Les trois dernières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 != 0:  # Cases noires
                plateau[a][i] = 2  # Pions noirs

def bouge_gauche():
    global screen, case_size, pion, pion_pos, nb_colonnes, marge_gauche, marge_haut, pion_ligne
    if pion_pos > 0 :
        dessine_plateau()
        pion_pos -= 1
    screen.blit(pion, (marge_gauche + pion_pos * case_size, marge_haut))

def bouge_droite():
    global screen, case_size, pion, pion_pos, nb_colonnes, marge_gauche, marge_droite, marge_haut, pion_ligne
    if pion_pos < nb_colonnes-1:
        dessine_plateau()
        pion_pos += 1
    screen.blit(pion, (marge_gauche + pion_pos * case_size, marge_haut))

def bouge_bas_droite():
    global pion_pos_x, pion_pos_y
    if pion_pos_x < nb_colonnes - 1 and pion_pos_y < nb_lignes - 1:
        pion_pos_x += 1
        pion_pos_y += 1


def bouge_bas_gauche():
    global pion_pos_x, pion_pos_y
    if pion_pos_x > 0 and pion_pos_y < nb_lignes - 1:
        pion_pos_x -= 1
        pion_pos_y += 1


def bouge_haut_droite():
    global pion_pos_x, pion_pos_y
    if pion_pos_x < nb_colonnes - 1 and pion_pos_y > 0:
        pion_pos_x += 1
        pion_pos_y -= 1


def bouge_haut_gauche():
    global pion_pos_x, pion_pos_y
    if pion_pos_x > 0 and pion_pos_y > 0:
        pion_pos_x -= 1
        pion_pos_y -= 1



def coordonnees_souris_to_case(pos):
    """Convertit les coordonnées de la souris en indices de case sur le plateau."""
    x, y = pos
    colonne = (x - marge_gauche) // case_size
    ligne = (y - marge_haut) // case_size
    if 0 <= colonne < nb_colonnes and 0 <= ligne < nb_lignes:
        return ligne, colonne
    return None

def deplacement_valide(ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee):
    """Vérifie si le déplacement est valide (diagonale et une seule case)."""
    return abs(ligne_arrivee - ligne_depart) == 1 and abs(colonne_arrivee - colonne_depart) == 1

# ------------ MAIN ------------

# Paramètres de base
case_size = 80
cases_blanches = (238, 227, 211)
cases_noires = (147, 119, 90)

# Marges autour du damier
marge_gauche = 100
marge_haut = 100

# Dimensions du plateau
nb_colonnes = 10
nb_lignes = 10
plateau = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

# Placement des pions
place_pions()

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
window_size = (case_size * nb_colonnes + marge_gauche * 2, case_size * nb_lignes + marge_haut * 2)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Jeu de Dames - Déplacement de Pions")

# Charger les images des pions
pion_noir = pygame.image.load('MA-24_pion.png')
pion_noir = pygame.transform.scale(pion_noir, (case_size, case_size))

pion_blanc = pygame.image.load('MA-24_pion-blanc.png')
pion_blanc = pygame.transform.scale(pion_blanc, (case_size, case_size))

# Variables pour gérer la sélection
pion_selectionne = None  # Stocke les coordonnées du pion sélectionné

# Dessiner le plateau initial
dessine_plateau()
pygame.display.flip()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche uniquement
            pos = pygame.mouse.get_pos()
            case = coordonnees_souris_to_case(pos)
            if case:
                ligne, colonne = case
                if pion_selectionne is None:  # Sélectionner un pion
                    if plateau[ligne][colonne] != 0:  # Case occupée par un pion
                        pion_selectionne = (ligne, colonne)
                else:  # Déplacer le pion
                    ligne_depart, colonne_depart = pion_selectionne
                    if plateau[ligne][colonne] == 0 and deplacement_valide(ligne_depart, colonne_depart, ligne, colonne):
                        plateau[ligne][colonne] = plateau[ligne_depart][colonne_depart]
                        plateau[ligne_depart][colonne_depart] = 0
                    pion_selectionne = None

    # Redessiner le plateau
    dessine_plateau()

    # Indiquer le pion sélectionné
    if pion_selectionne:
        ligne, colonne = pion_selectionne
        x = marge_gauche + colonne * case_size
        y = marge_haut + ligne * case_size
        pygame.draw.rect(screen, (0, 255, 0), (x, y, case_size, case_size), 5)

    pygame.display.flip()

pygame.quit()