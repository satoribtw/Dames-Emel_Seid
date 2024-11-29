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
    - Trois dernières lignes : pions noirs sur cases blanches.
    """
    for a in range(3):  # Les trois premières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 != 0:  # Cases noires
                plateau[a][i] = 1  # Pions blancs

    for a in range(nb_lignes - 3, nb_lignes):  # Les trois dernières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 == 0:  # Cases blanches
                plateau[a][i] = 2  # Pions noirs


# ------------
# --- MAIN ---
# ------------

# Paramètres de base
case_size = 80
cases_blanches = (238, 227, 211)
cases_noires = (147, 119, 90)
window_color = (89, 152, 255)

# Marges autour du damier
marge_gauche = 10
marge_droite = 10
marge_haut = 10
marge_bas = 10

# Dimensions du plateau
nb_colonnes = 10
nb_lignes = 10

# Plateau : 0 = vide, 1 = pion blanc, 2 = pion noir
plateau = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]

# Placement des pions
place_pions()

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
window_size = (case_size * nb_colonnes + marge_gauche + marge_droite,
               case_size * nb_lignes + marge_haut + marge_bas)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Jeu de Dames - Placement de Pions")

# Charger les images des pions
pion_noir = pygame.image.load('MA-24_pion.png')
pion_noir = pygame.transform.scale(pion_noir, (case_size, case_size))

pion_blanc = pygame.image.load('MA-24_pion-blanc.png')
pion_blanc = pygame.transform.scale(pion_blanc, (case_size, case_size))

# Dessiner le plateau initial
dessine_plateau()
pygame.display.flip()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
