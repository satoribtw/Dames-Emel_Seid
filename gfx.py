#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------1---------2---------3---------4---------5---------6---------7---------8
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
Name : main.py
Authors : Emel Keres and Seid Fejzulahi
Date : 2025.01.17
Version : Final
Purpose : Le dessin du plateau

---------------------------------------------------------------------------

  # 2025-01-17 03 EMK and SFI
  - Changement dans la boucle principal

Fait par Seid et Emel

"""


import pygame

def dessine_plateau(screen, plateau, nb_colonnes, nb_lignes, case_size, marge_gauche, marge_haut, cases_blanches, cases_noires, pion_blanc, pion_noir, dame_blanche, dame_noire):
    """
    Dessine le damier et place les pions ou dames si présents.
    """
    for i in range(nb_colonnes):
        for a in range(nb_lignes):
            x = marge_gauche + i * case_size
            y = marge_haut + a * case_size
            couleur = cases_blanches if (i + a) % 2 == 0 else cases_noires
            pygame.draw.rect(screen, couleur, (x, y, case_size, case_size))

            # Dessiner les pions et dames
            if plateau[a][i] == 1:  # Pion blanc
                screen.blit(pion_blanc, (x, y))
            elif plateau[a][i] == 2:  # Pion noir
                screen.blit(pion_noir, (x, y))
            elif plateau[a][i] == 3:  # Dame blanche
                screen.blit(dame_blanche, (x, y))
            elif plateau[a][i] == 4:  # Dame noire
                screen.blit(dame_noire, (x, y))

