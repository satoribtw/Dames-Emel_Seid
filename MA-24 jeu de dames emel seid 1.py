"""
Name    : MA-24 jeu de dames emel seid.py
Authors : Emel Keres
Date    : 2024.11.15
Version : 0.01
Purpose : Jeu de dames avec la librairie pygamek,

"""

import pygame



def bouge_gauche():
    global screen, case_size, pion, pion_pos, nb_colonnes, marge_gauche, marge_haut
    if pion_pos > 0 :
        dessine_case(pion_pos)
        pion_pos -= 1
    screen.blit(pion, (marge_gauche + pion_pos*case_size, marge_haut))

def bouge_droite():
    global screen, case_size, pion, pion_pos, nb_colonnes, marge_gauche, marge_droite, marge_haut
    if pion_pos < nb_colonnes-1:
        dessine_case(pion_pos)
        pion_pos += 1
    screen.blit(pion, (marge_gauche + pion_pos*case_size, marge_haut))

def dessine_case(case_pos):
    """Dessine la xème case du damier
    """
    global screen, case_size, cases_blanches, cases_noires, marge_gauche, marge_haut, bouge_gauche, bouge_droite
    if case_pos % 2:
        pygame.draw.rect(screen, cases_blanches,
        (marge_gauche + case_pos*case_size,
              marge_haut,
              case_size,
              case_size),
              0)
    else:
        pygame.draw.rect(screen, cases_noires,
        (marge_gauche + case_pos*case_size,
              marge_haut,
              case_size,
              case_size),
              0)



# ------------
# --- MAIN ---
# ------------

            # ERREUR 
plateau =   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]


# Version pygame
case_size = 80
cases_blanches = (255, 255, 255)
cases_noires = (180, 180, 180)
pions_blancs = (255, 255, 255)
pions_noirs = (0, 0, 0)

# Marges autour du damier
marge_gauche = 10
marge_droite = 10
marge_haut = 10
marge_bas = 10


pion_pos = 0


path_to_images = "pictures\\"
pygame.init()

# Window size x, y
nb_colonnes = len(plateau)
window_size = (case_size*nb_colonnes
               + marge_gauche
               + marge_droite,
               case_size
               + marge_haut
               + marge_bas
               )
window_color = (89, 152, 255)
screen = pygame.display.set_mode(window_size)
icon = pygame.image.load('International_draughts.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("MA-24 : Jeu de Dames")
screen.fill(window_color)

# Affiche le damier
for case in range(nb_colonnes):
    dessine_case(case)

# Charge l'image du pion
pion = pygame.image.load('MA-24_pion.png')
pion = pygame.transform.scale(pion, (case_size, case_size))
screen.blit(pion, (marge_gauche, marge_haut))
pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        btn_presse = pygame.key.get_pressed()
        if btn_presse[pygame.K_RIGHT]:
            bouge_droite()
        elif btn_presse[pygame.K_LEFT]:
            bouge_gauche()
        elif btn_presse[pygame.K_q]:
            running = False
        pygame.display.update()

pygame.quit()
