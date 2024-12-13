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

# Vérifie si le mouvement est valide
def mouvement_valide(x1, y1, x2, y2, joueur):
    if 0 <= x2 < nb_colonnes and 0 <= y2 < nb_lignes and plateau[y2][x2] == 0:
        if joueur == 1 and y2 == y1 - 1 and abs(x2 - x1) == 1:
            return True
        elif joueur == 2 and y2 == y1 + 1 and abs(x2 - x1) == 1:
            return True
    return False

# Déplace un pion sur le plateau
def deplace_pion(x1, y1, x2, y2):
    plateau[y2][x2] = plateau[y1][x1]
    plateau[y1][x1] = 0

# Déplace un pion en fonction des touches de direction
def deplace_avec_fleches(selection, direction, joueur):
    if selection:
        x1, y1 = selection
        if direction == "haut_gauche":
            x2, y2 = x1 - 1, y1 - 1
        elif direction == "haut_droite":
            x2, y2 = x1 + 1, y1 - 1
        elif direction == "bas_gauche":
            x2, y2 = x1 - 1, y1 + 1
        elif direction == "bas_droite":
            x2, y2 = x1 + 1, y1 + 1
        else:
            return selection

        if mouvement_valide(x1, y1, x2, y2, joueur):
            deplace_pion(x1, y1, x2, y2)
            return None  # Déselectionner le pion après déplacement
    return selection

# ------------ MAIN ------------

# Paramètres de base
case_size = 80
cases_blanches = (238, 227, 211)
cases_noires = (147, 119, 90)
bleu = (0, 0, 0)

# Marges autour du damier
marge_gauche = 100
marge_droite = 100
marge_haut = 100
marge_bas = 100

# Dimensions du plateau
nb_colonnes = 10
nb_lignes = 10
pion_ligne = 9
pion_pos = 0
pions_pos_x = 0
pions_pos_y = 0
pion_noir_pos_x = 0
pion_noir_pos_y = 0

# Plateau : 0 = vide, 1 = pion blanc, 2 = pion noir
plateau = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

# Placement des pions
place_pions()


pygame.init()
window_size = (case_size * nb_colonnes + marge_gauche + marge_droite, case_size * nb_lignes + marge_haut + marge_bas)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Jeu de Dames - Placement de Pions")

# Charger l'image de fond
background_image = pygame.image.load('a52a2a.png')  # Remplacez 'background.jpg' par le chemin de votre image
background_image = pygame.transform.scale(background_image, window_size)  # Redimensionner l'image à la taille de la fenêtre
# Après l'initialisation de Pygame
# Création de la police pour le texte
font = pygame.font.Font(None, 36)  # None pour la police par défaut, 36 est la taille du texte
texte = font.render("Jeu de Dames", True, bleu)  # Texte à afficher en rouge
texte_rect = texte.get_rect()
texte_rect.topright = (window_size[0] - 20, 20)  # Position du texte en haut à droite

# Dans la boucle principale, après dessine_plateau()
screen.blit(texte, texte_rect)  # Affiche le texte sur l'écran

# Charger les images des pions
pion_noir = pygame.image.load('MA-24_pion.png')
pion_noir = pygame.transform.scale(pion_noir, (case_size, case_size))

pion_blanc = pygame.image.load('MA-24_pion-blanc.png')
pion_blanc = pygame.transform.scale(pion_blanc, (case_size, case_size))

# Dessiner le plateau initial avec une image de fond
screen.blit(background_image, (0, 0))
screen.blit(texte, texte_rect)# Afficher l'image de fond
dessine_plateau()
pygame.display.flip()

# Variables de jeu
joueur_actuel = 1  # 1 = blanc, 2 = noir
selection = None
joueur_actuel = 2

# Boucle principale
running = True
while running:
    dessine_plateau()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selection = deplace_avec_fleches(selection, "haut_gauche" if joueur_actuel == 1 else "bas_gauche", joueur_actuel)
                joueur_actuel = 3 - joueur_actuel if not selection else joueur_actuel
            elif event.key == pygame.K_RIGHT:
                selection = deplace_avec_fleches(selection, "haut_droite" if joueur_actuel == 1 else "bas_droite", joueur_actuel)
                joueur_actuel = 3 - joueur_actuel if not selection else joueur_actuel

pygame.quit()