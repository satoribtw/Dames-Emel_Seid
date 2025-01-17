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
    Vérifie si une capture est valide et effectue la capture si c'est le cas.
    """
    if (
        abs(ligne_arrivee - ligne_depart) == 2 and  # Déplacement de deux cases
        abs(colonne_arrivee - colonne_depart) == 2  # Déplacement diagonal
    ):
        ligne_milieu = (ligne_depart + ligne_arrivee) // 2
        colonne_milieu = (colonne_depart + colonne_arrivee) // 2

        # Vérifier si la case intermédiaire contient un pion adverse
        if (
            plateau[ligne_milieu][colonne_milieu] != 0 and
            plateau[ligne_milieu][colonne_milieu] not in [current_player, current_player + 2] and
            plateau[ligne_arrivee][colonne_arrivee] == 0  # La case d'arrivée doit être vide
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

def deplacement_dame_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee):
    """
    Vérifie si un déplacement de dame est valide (diagonale libre et toutes les cases entre départ et arrivée sont vides).
    """
    # Vérifier si c'est bien un déplacement en diagonale
    if abs(ligne_arrivee - ligne_depart) != abs(colonne_arrivee - colonne_depart):
        return False  # Pas un déplacement en diagonale

    # Déterminer la direction du déplacement
    delta_ligne = 1 if ligne_arrivee > ligne_depart else -1
    delta_colonne = 1 if colonne_arrivee > colonne_depart else -1

    # Parcourir les cases intermédiaires sur la diagonale
    ligne, colonne = ligne_depart + delta_ligne, colonne_depart + delta_colonne
    while (ligne, colonne) != (ligne_arrivee, colonne_arrivee):
        if plateau[ligne][colonne] != 0:
            return False  # Une case intermédiaire est occupée
        ligne += delta_ligne
        colonne += delta_colonne

def capture_dame_valide(plateau, ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee, current_player):
    """
    Vérifie si une capture par une dame est valide.
    La dame peut capturer un pion adverse, même s'il est éloigné,
    tant que la case après lui est vide et qu'il n'y a pas d'autres pions entre les deux.
    """
    # Vérifier si c'est bien un déplacement en diagonale
    if abs(ligne_arrivee - ligne_depart) != abs(colonne_arrivee - colonne_depart):
        return False  # Pas un déplacement en diagonale

    # Déterminer la direction du déplacement
    delta_ligne = 1 if ligne_arrivee > ligne_depart else -1
    delta_colonne = 1 if colonne_arrivee > colonne_depart else -1

    # Variables pour suivre les cases sur la diagonale
    ligne, colonne = ligne_depart + delta_ligne, colonne_depart + delta_colonne
    pions_adverses = 0
    ligne_pion_capture = colonne_pion_capture = None

    # Parcourir les cases intermédiaires sur la diagonale
    while (ligne, colonne) != (ligne_arrivee, colonne_arrivee):
        if plateau[ligne][colonne] != 0:  # Une pièce est trouvé
            if plateau[ligne][colonne] != current_player and pions_adverses == 0:
                # Premier pion adverse trouvé
                pions_adverses += 1
                ligne_pion_capture, colonne_pion_capture = ligne, colonne
            else:
                # Plus d'un pion ou une pièce alliée bloque le chemin
                return False
        ligne += delta_ligne
        colonne += delta_colonne

    # Vérifier les conditions finales pour la capture
    if (
        pions_adverses == 1 and  # Il doit y avoir exactement un pion adverse
        plateau[ligne_arrivee][colonne_arrivee] == 0  # La case d'arrivée doit être vide
    ):
        # Effectuer la capture
        plateau[ligne_pion_capture][colonne_pion_capture] = 0  # Retirer le pion capturé
        plateau[ligne_arrivee][colonne_arrivee] = plateau[ligne_depart][colonne_depart]  # Déplacer la dame
        plateau[ligne_depart][colonne_depart] = 0  # Vider la case de départ
        return True

    return False


def changer_joueur(current_player):
    """Alterner entre les joueurs."""
    return 2 if current_player == 1 else 1