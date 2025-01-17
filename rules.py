def place_pions(plateau, nb_colonnes, nb_lignes):
    """
    Place les pions sur les trois premières et trois dernières lignes.
    """
    for a in range(4):  # Les trois premières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 != 0:  # Cases noires
                plateau[a][i] = 1  # Pions blancs

    for a in range(nb_lignes - 4, nb_lignes):  # Les trois dernières lignes
        for i in range(nb_colonnes):
            if (i + a) % 2 != 0:  # Cases noires
                plateau[a][i] = 2  # Pions noirs

def coordonnees_souris_to_case(pos, marge_gauche, marge_haut, case_size, nb_colonnes, nb_lignes):
    """Convertit les coordonnées de la souris en indices de case sur le plateau."""
    x, y = pos
    colonne = (x - marge_gauche) // case_size
    ligne = (y - marge_haut) // case_size
    if 0 <= colonne < nb_colonnes and 0 <= ligne < nb_lignes:
        return ligne, colonne
    return None

def deplacement_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee):
    """Vérifie si le déplacement est valide (diagonale et une seule case)."""
    return (
        abs(ligne_arrivee - ligne_depart) == 1 and
        abs(colonne_arrivee - colonne_depart) == 1 and
        plateau[ligne_arrivee][colonne_arrivee] == 0
    )

def deplacement_direction_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee, current_player):
    """
    Vérifie si le déplacement est dans la bonne direction :
    - Les pions blancs (1) ne peuvent avancer que vers le bas.
    - Les pions noirs (2) ne peuvent avancer que vers le haut.
    - Les dames (3, 4) peuvent se déplacer dans toutes les directions.
    - Le déplacement vers l'arrière est permis uniquement en cas de capture.
    """
    delta_ligne = ligne_arrivee - ligne_depart
    delta_colonne = colonne_arrivee - colonne_depart

    # Vérifier si c'est un déplacement arrière
    is_backward = (current_player == 1 and delta_ligne < 0) or (current_player == 2 and delta_ligne > 0)

    if plateau[ligne_depart][colonne_depart] in [1, 2]:  # Pion
        if is_backward:
            # Autoriser uniquement si c'est une capture
            return (
                abs(delta_ligne) == 2 and
                abs(delta_colonne) == 2 and
                plateau[(ligne_depart + ligne_arrivee) // 2][(colonne_depart + colonne_arrivee) // 2] not in [0, current_player]
            )
        # Déplacement normal (vers l'avant uniquement)
        return abs(delta_ligne) == 1 and abs(delta_colonne) == 1

    elif plateau[ligne_depart][colonne_depart] in [3, 4]:  # Dame
        # Les dames peuvent se déplacer dans toutes les directions
        return abs(delta_ligne) == abs(delta_colonne)  # Déplacement en diagonale

    return False

def capture_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee, current_player):
    """
    Vérifie si une capture par un pion est valide et effectue la capture si c'est le cas.
    """
    if abs(ligne_arrivee - ligne_depart) == 2 and abs(colonne_arrivee - colonne_depart) == 2:
        ligne_milieu = (ligne_depart + ligne_arrivee) // 2
        colonne_milieu = (colonne_depart + colonne_arrivee) // 2

        # Vérifier si la case intermédiaire contient un pion adverse
        if (
            plateau[ligne_milieu][colonne_milieu] not in [0, current_player, current_player + 2] and
            plateau[ligne_arrivee][colonne_arrivee] == 0
        ):
            # Effectuer la capture
            plateau[ligne_milieu][colonne_milieu] = 0  # Retirer le pion capturé
            plateau[ligne_arrivee][colonne_arrivee] = plateau[ligne_depart][colonne_depart]  # Déplacer le pion
            plateau[ligne_depart][colonne_depart] = 0  # Vider la case de départ
            return True

    return False

def captures_possibles(plateau, ligne, colonne, current_player):
    """
    Vérifie si des captures multiples sont possibles pour un pion ou une dame.
    """
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Diagonales possibles pour la capture
    for direction in directions:
        ligne_arrivee = ligne + direction[0]
        colonne_arrivee = colonne + direction[1]
        if (
            0 <= ligne_arrivee < len(plateau) and
            0 <= colonne_arrivee < len(plateau[0]) and
            capture_valide(plateau, ligne, colonne, ligne_arrivee, colonne_arrivee, current_player)
        ):
            return True
    return False

def promotion_dame(plateau, nb_colonnes, nb_lignes):
    """
    Transforme un pion en dame lorsqu'il atteint le bord opposé.
    """
    # Vérifier les pions blancs qui atteignent le dernier rang
    for i in range(nb_colonnes):
        if plateau[nb_lignes - 1][i] == 1:  # Pion blanc
            plateau[nb_lignes - 1][i] = 3  # Devenir dame blanche

    # Vérifier les pions noirs qui atteignent le premier rang
    for i in range(nb_colonnes):
        if plateau[0][i] == 2:  # Pion noir
            plateau[0][i] = 4  # Devenir dame noire

def capture_dame_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee, joueur):
    """
    Vérifie si une capture par une dame est valide et effectue la capture si c'est le cas.
    """
    delta_ligne = ligne_arrivee - ligne_depart
    delta_colonne = colonne_arrivee - colonne_depart

    # Vérifier que le déplacement est diagonal
    if abs(delta_ligne) != abs(delta_colonne):
        return False

    # Vérifier qu'il n'y a qu'une seule pièce adverse sur le chemin
    direction_ligne = 1 if delta_ligne > 0 else -1
    direction_colonne = 1 if delta_colonne > 0 else -1
    pieces_trouvees = 0
    ligne_captured = colonne_captured = None  # Coordonnées du pion capturé

    for i in range(1, abs(delta_ligne)):
        x = ligne_depart + i * direction_ligne
        y = colonne_depart + i * direction_colonne
        print(f"Inspecting cell: ({x}, {y}), value: {plateau[x][y]}")  # Debugging info
        if plateau[x][y] == joueur or plateau[x][y] == joueur + 2:  # Pièce alliée
            return False
        elif plateau[x][y] != 0:  # Pièce adverse
            pieces_trouvees += 1
            ligne_captured, colonne_captured = x, y
            if pieces_trouvees > 1:
                return False

    # Effectuer la capture si valide
    if pieces_trouvees == 1:
        print(f"Capturing piece at: ({ligne_captured}, {colonne_captured})")  # Debugging info
        plateau[ligne_captured][colonne_captured] = 0  # Supprimer le pion capturé
        plateau[ligne_arrivee][colonne_arrivee] = plateau[ligne_depart][colonne_depart]  # Déplacer la dame
        plateau[ligne_depart][colonne_depart] = 0  # Vider la case de départ
        return True

    return False

def changer_joueur(current_player):
    """Alterner entre les joueurs."""
    return 2 if current_player == 1 else 1