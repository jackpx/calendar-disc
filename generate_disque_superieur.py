import math
import matplotlib.pyplot as plt

# -----------------------------
# Paramètres généraux
# -----------------------------
MM = 1 / 25.4
SIZE_MM = 200
SIZE_IN = SIZE_MM * MM

NB_SECTEURS = 28
ANGLE_SECTEUR = 2 * math.pi / NB_SECTEURS

# Rotation d'un demi-secteur (sens corrigé)
ROT = +0.5 * ANGLE_SECTEUR

# Rayon de référence (identique au disque principal)
R_JOURS = 40 / 100.0

# Bord extérieur du disque secondaire
R_CERCLE_EXT = 0.95

# Couronne identique au disque principal
R_COURONNE_INF = R_JOURS - 0.5 * MM
R_COURONNE_SUP = R_JOURS + 0.7 * MM

# Secteurs du bas : indices 17 → 23
SECTEURS_BAS = range(17, 24)

# Secteurs du haut : indices 3 → 9
SECTEURS_HAUT = range(3, 10)

# Jours par secteur bas
JOURS_SECTEURS = {
    17: [1, 8, 15, 22, 29],
    18: [2, 9, 16, 23, 30],
    19: [3, 10, 17, 24, 31],
    20: [4, 11, 18, 25],
    21: [5, 12, 19, 26],
    22: [6, 13, 20, 27],
    23: [7, 14, 21, 28],
}

# Mois par colonne (droite → gauche)
MOIS_PAR_SECTEUR = {
    9: ["MAI"],
    8: ["AOUT", "FEV"],        # FEV normal (noir)
    7: ["FEV", "MARS", "NOV"], # FEV (bis) → rouge
    6: ["JUIN"],
    5: ["SEPT", "DEC"],
    4: ["AVR", "JUIL", "JAN"], # JAN (bis) → rouge
    3: ["JANV", "OCT"],
}

# -----------------------------
# Génération du PDF
# -----------------------------
def genere_disque_secondaire(nom="disque_secondaire.pdf"):
    fig, ax = plt.subplots(figsize=(SIZE_IN, SIZE_IN))
    ax.set_aspect("equal")
    ax.axis("off")

    def arc(rayon, th1, th2):
        T = [th1 + k*(th2-th1)/80 for k in range(81)]
        return [rayon * math.cos(t) for t in T], [rayon * math.sin(t) for t in T]

    # --- Couronne bas (sup + inf) ---
    for i in SECTEURS_BAS:
        th1 = i * ANGLE_SECTEUR + ROT
        th2 = (i + 1) * ANGLE_SECTEUR + ROT
        x, y = arc(R_COURONNE_SUP, th1, th2)
        ax.plot(x, y, color="black", linewidth=0.8)
        x, y = arc(R_COURONNE_INF, th1, th2)
        ax.plot(x, y, color="black", linewidth=0.8)

    # --- Couronne haut : arc supérieur seulement ---
    for i in SECTEURS_HAUT:
        th1 = i * ANGLE_SECTEUR + ROT
        th2 = (i + 1) * ANGLE_SECTEUR + ROT
        x, y = arc(R_COURONNE_SUP, th1, th2)
        ax.plot(x, y, color="black", linewidth=0.8)

    # --- Rayons bas ---
    for i in SECTEURS_BAS:
        th = i * ANGLE_SECTEUR + ROT
        x1 = R_COURONNE_INF * math.cos(th)
        y1 = R_COURONNE_INF * math.sin(th)
        x2 = R_CERCLE_EXT * math.cos(th)
        y2 = R_CERCLE_EXT * math.sin(th)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.8)

    # Bord droit du dernier secteur bas
    th_last = 24 * ANGLE_SECTEUR + ROT
    ax.plot(
        [R_COURONNE_INF * math.cos(th_last), R_CERCLE_EXT * math.cos(th_last)],
        [R_COURONNE_INF * math.sin(th_last), R_CERCLE_EXT * math.sin(th_last)],
        color="black", linewidth=0.8
    )

    # --- Rayons haut (3 gauche, 9 droite) ---
    for th in [3 * ANGLE_SECTEUR + ROT, 10 * ANGLE_SECTEUR + ROT]:
        x1 = R_COURONNE_SUP * math.cos(th)
        y1 = R_COURONNE_SUP * math.sin(th)
        x2 = R_CERCLE_EXT * math.cos(th)
        y2 = R_CERCLE_EXT * math.sin(th)
        ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.8)

    # --- Texte : jours dans les 7 secteurs bas ---
    for i in SECTEURS_BAS:
        jours = JOURS_SECTEURS[i]
        th = (i + 0.5) * ANGLE_SECTEUR + ROT
        for k, jour in enumerate(jours):
            r = R_COURONNE_INF + (4 + 2.2 * k) * MM   # rapproché de 1 mm
            x = r * math.cos(th)
            y = r * math.sin(th)
            phi = th + math.pi/2
            if math.cos(phi) < 0:
                phi += math.pi
            ax.text(
                x, y, str(jour),
                ha="center", va="center",
                fontsize=7,
                rotation=math.degrees(phi),
                rotation_mode="anchor"
            )

    # --- Colonnes de mois (verticales) ---
    hauteur_colonne = 9.5 * MM   # diminuée de 2.5 mm

    for i in SECTEURS_HAUT:
        if i not in MOIS_PAR_SECTEUR:
            continue

        mois = MOIS_PAR_SECTEUR[i]

        # angles des bords du secteur
        th_left  = i * ANGLE_SECTEUR + ROT
        th_right = (i + 1) * ANGLE_SECTEUR + ROT

        # bords verticaux
        for th in [th_left, th_right]:
            x = R_COURONNE_SUP * math.cos(th)
            y_top = R_COURONNE_SUP * math.sin(th)
            y_bottom = y_top - hauteur_colonne
            ax.plot([x, x], [y_top, y_bottom], color="black", linewidth=0.6)

        # colonne interne pour le texte
        th_mid = (i + 0.5) * ANGLE_SECTEUR + ROT
        x0 = R_COURONNE_SUP * math.cos(th_mid)
        y0 = R_COURONNE_SUP * math.sin(th_mid)

        for k, m in enumerate(mois):
            y = y0 - (2.5 * MM) - (k * 3 * MM)

            # RÈGLE EXACTE :
            # - FEV normal (secteur 8) → noir
            # - FEV (bis) (secteur 7) → rouge
            # - JAN (bis) (secteur 4) → rouge
            if i == 8 and m == "FEV":
                color = "black"
            elif i == 7 and m == "FEV":
                color = "red"
            elif i == 4 and m == "JAN":
                color = "red"
            else:
                color = "black"

            ax.text(
                x0, y, m,
                ha="center", va="center",
                fontsize=7,
                rotation=30,
                color=color,
                rotation_mode="anchor"
            )

    # --- Cercle extérieur ---
    theta_full = [i * 2*math.pi/360 for i in range(361)]
    ax.plot(
        [R_CERCLE_EXT * math.cos(t) for t in theta_full],
        [R_CERCLE_EXT * math.sin(t) for t in theta_full],
        color="black", linewidth=0.8
    )

    # --- Point central ---
    centre = plt.Circle((0, 0), 1.5 * MM, color="white", ec="black", linewidth=0.8)
    ax.add_artist(centre)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    fig.savefig(nom, dpi=300, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    genere_disque_secondaire()
    print("PDF généré : disque_secondaire.pdf")
