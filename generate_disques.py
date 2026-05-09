import math
import datetime
import matplotlib.pyplot as plt

# -----------------------------
# Paramètres généraux
# -----------------------------
MM = 1 / 25.4
SIZE_MM = 200
SIZE_IN = SIZE_MM * MM

NB_SECTEURS = 28
ANGLE_SECTEUR = 2 * math.pi / NB_SECTEURS

R_JOURS = 40 / 100.0        # rayon des lettres des jours (avant décalage)
R_JOURS_DECALE = R_JOURS + 0.3 * MM   # +0,1 mm vers l'extérieur

R_CERCLE_EXT = 0.95         # bord extérieur du disque

# Cercles de la couronne des jours
R_COURONNE_INF = R_JOURS - 0.5 * MM
R_COURONNE_SUP = R_JOURS + 0.7 * MM

# Jours répétés 4 fois
JOURS = ["L", "M", "M", "J", "V", "S", "D"] * 4

AN_DEBUT = 1844
AN_FIN = 2118

# -----------------------------
# Fonctions utilitaires
# -----------------------------
def est_bissextile(a):
    return (a % 4 == 0 and (a % 100 != 0 or a % 400 == 0))

def construit_liste_annees():
    L = []
    for a in range(AN_DEBUT, AN_FIN + 1):
        if est_bissextile(a):
            L.append(None)   # case vide AVANT l'année bissextile
        L.append(a)
    return L

# -----------------------------
# Génération du PDF
# -----------------------------
def genere_disque_spirale_pdf(nom="disque_spirale.pdf"):
    fig, ax = plt.subplots(figsize=(SIZE_IN, SIZE_IN))
    ax.set_aspect("equal")
    ax.axis("off")

    theta = [i * 2*math.pi/360 for i in range(361)]

    # --- Cercles de la couronne des jours ---
    ax.plot([R_CERCLE_EXT * math.cos(t) for t in theta],
            [R_CERCLE_EXT * math.sin(t) for t in theta],
            color="black", linewidth=0.8)

    ax.plot([R_COURONNE_SUP * math.cos(t) for t in theta],
            [R_COURONNE_SUP * math.sin(t) for t in theta],
            color="black", linewidth=0.8)

    ax.plot([R_COURONNE_INF * math.cos(t) for t in theta],
            [R_COURONNE_INF * math.sin(t) for t in theta],
            color="black", linewidth=0.8)

    # --- Rayons ---
    for i in range(NB_SECTEURS):
        th = i * ANGLE_SECTEUR
        x2 = R_CERCLE_EXT * math.cos(th)
        y2 = R_CERCLE_EXT * math.sin(th)
        ax.plot([0, x2], [0, y2], color="black", linewidth=0.4)

    # --- Initiales des jours (haut vers le centre, perpendiculaire au rayon) ---
    for i in range(NB_SECTEURS):
        th = (i + 0.5) * ANGLE_SECTEUR

        # position décalée de 0,1 mm vers l'extérieur
        x = R_JOURS_DECALE * math.cos(th)
        y = R_JOURS_DECALE * math.sin(th)

        # orientation : perpendiculaire au rayon, haut vers le centre
        phi = th + math.pi/2
        angle_deg = math.degrees(phi)

        ax.text(
            x, y, JOURS[i],
            ha="center", va="center",
            fontsize=10,
            rotation=angle_deg,
            rotation_mode="anchor"
        )

    # --- Spirale des années ---
    annees = construit_liste_annees()
    N = len(annees)

    r_start = R_CERCLE_EXT - 0.03
    r_end = R_COURONNE_SUP + 0.03

    start_sector = 0  # LUNDI → pour que 1844 tombe sur MARDI

    points = []
    for k in range(N):
        t = 1 - k / (N - 1)
        r = r_start - (r_start - r_end) * t
        secteur = (start_sector + k) % NB_SECTEURS
        theta_secteur = (secteur + 0.5) * ANGLE_SECTEUR
        x = r * math.cos(theta_secteur)
        y = r * math.sin(theta_secteur)
        points.append((x, y))

    for k, an in enumerate(annees):
        if an is None:
            continue

        x, y = points[k]
        theta = math.atan2(y, x)

        # orientation : perpendiculaire au rayon, BAS vers le centre
        phi = theta + math.pi/2 + math.pi
        angle_deg = math.degrees(phi)

        color = "red" if est_bissextile(an) else "black"

        ax.text(
            x, y, str(an),
            ha="center", va="center",
            fontsize=6, color=color,
            rotation=angle_deg,
            rotation_mode="anchor"
        )

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    fig.savefig(nom, dpi=300, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    genere_disque_spirale_pdf()
    print("PDF généré : disque_spirale.pdf")
