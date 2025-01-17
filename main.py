#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Name : main.py
Authors : Emel Keres and Seid Fejzulahi
Date : 2025.01.17
Version : Final
Purpose : Boucle principal du jeu avec l'interface du plateau et le nombre de joueur afficher, les pions noirs et blancs, dames

---------------------------------------------------------------------------

  # 2025-01-17 03 EMK and SFI
  - Changement dans la boucle principal
"""

import pygame
import gfx
import rules

# Paramètres de base
# Fait par Emel et Seid
case_size = 80
cases_blanches = (238, 227, 211)
cases_noires = (147, 119, 90)
marge_gauche = 100
marge_haut = 100
nb_colonnes = 10
nb_lignes = 10
plateau = [[0 for _ in range(nb_colonnes)] for _ in range(nb_lignes)]
rules.place_pions(plateau, nb_colonnes, nb_lignes)

# Initialisation de Pygame
pygame.init()
window_size = (case_size * nb_colonnes + marge_gauche * 2, case_size * nb_lignes + marge_haut * 2 + 50)  # Espace pour afficher le texte
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Jeu de Dames - Déplacement de Pions et Dames")

# Chargement des images
pion_noir = pygame.image.load('MA-24_pion_noir.png')
pion_noir = pygame.transform.scale(pion_noir, (case_size, case_size))

pion_blanc = pygame.image.load('MA-24_pion-blanc.png')
pion_blanc = pygame.transform.scale(pion_blanc, (case_size, case_size))

dame_noire = pygame.image.load('MA-24_dame_noire.png')
dame_noire = pygame.transform.scale(dame_noire, (case_size, case_size))

dame_blanche = pygame.image.load('MA-24_dame_blanche.png')
dame_blanche = pygame.transform.scale(dame_blanche, (case_size, case_size))

# Variables pour le jeu
pion_selectionne = None
current_player = 1

# Création de la police pour afficher le texte
font = pygame.font.Font(None, 36)

# Dessin initial du plateau
gfx.dessine_plateau(screen, plateau, nb_colonnes, nb_lignes, case_size, marge_gauche, marge_haut, cases_blanches, cases_noires, pion_blanc, pion_noir, dame_blanche, dame_noire)

# Afficher le joueur actuel
text = font.render(f"Joueur : {current_player}", True, (255, 255, 255))  # Texte avec la couleur blanche
screen.blit(text, (marge_gauche, marge_haut - 40))  # Afficher en haut du plateau
pygame.display.flip()

# Fait par ChatGPT
# la boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            case = rules.coordonnees_souris_to_case(pos, marge_gauche, marge_haut, case_size, nb_colonnes, nb_lignes)
            if case:
                ligne, colonne = case
                if pion_selectionne is None:
                    # Sélection d'un pion ou d'une dame
                    if plateau[ligne][colonne] in [current_player, current_player + 2]:  # Pion ou dame du joueur actuel
                        pion_selectionne = (ligne, colonne)
                else:
                    ligne_depart, colonne_depart = pion_selectionne
                    # Si on clique sur un autre pion/dame du joueur, changer la sélection
                    if plateau[ligne][colonne] in [current_player, current_player + 2]:
                        pion_selectionne = (ligne, colonne)
                    # Capture multiple
                    elif rules.capture_valide(plateau, ligne_depart, colonne_depart, ligne, colonne, current_player):
                        pion_selectionne = (ligne, colonne)
                        if not rules.captures_possibles(plateau, ligne, colonne, current_player):
                            rules.promotion_dame(plateau, nb_colonnes, nb_lignes)  # Vérifier promotion
                            current_player = rules.changer_joueur(current_player)
                            pion_selectionne = None
                    # Déplacement simple ou déplacement d'une dame avec validation directionnelle
                    elif (
                        rules.deplacement_direction_valide(plateau, ligne_depart, colonne_depart, ligne, colonne, current_player) and
                        (
                            rules.deplacement_valide(plateau, ligne_depart, colonne_depart, ligne, colonne) or
                            (plateau[ligne_depart][colonne_depart] in [3, 4] and rules.deplacement_direction_valide(plateau, ligne_depart, colonne_depart, ligne, colonne, current_player))
                        )
                    ):
                        plateau[ligne][colonne] = plateau[ligne_depart][colonne_depart]
                        plateau[ligne_depart][colonne_depart] = 0
                        rules.promotion_dame(plateau, nb_colonnes, nb_lignes)  # Vérifier promotion
                        current_player = rules.changer_joueur(current_player)
                        pion_selectionne = None

    # Redessiner le plateau après chaque mouvement
    screen.fill((0, 0, 0))  # Effacer l'écran pour redessiner
    gfx.dessine_plateau(screen, plateau, nb_colonnes, nb_lignes, case_size, marge_gauche, marge_haut, cases_blanches, cases_noires, pion_blanc, pion_noir, dame_blanche, dame_noire)

    # Afficher le joueur actuel
    text = font.render(f"Joueur : {current_player}", True, (255, 255, 255))  # Texte avec la couleur blanche
    screen.blit(text, (marge_gauche, marge_haut - 40))  # Afficher en haut du plateau

    # Afficher le pion sélectionné
    if pion_selectionne:
        ligne, colonne = pion_selectionne
        x = marge_gauche + colonne * case_size
        y = marge_haut + ligne * case_size
        pygame.draw.rect(screen, (0, 255, 0), (x, y, case_size, case_size), 5)

    pygame.display.flip()

pygame.quit()