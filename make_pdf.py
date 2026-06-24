from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm, mm
import os

# Couleurs
BLUE = HexColor('#005EA4')
ORANGE = HexColor('#E8520A')
LIGHT_BLUE = HexColor('#E8F2FB')
DARK_GRAY = HexColor('#333333')
MID_GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#F5F5F5')

# Chemins (à adapter si nécessaire)
SRC = ''          # dossier des images de secteurs, logo, etc.
LOGO_DIR = ''     # dossier des logos des marques
OUT = 'offre_service_eco_air.pdf'

width, height = A4
MARGIN = 40
CONTENT_W = width - 2 * MARGIN

def draw_section_title(c, y, number, title):
    """Dessine un titre de section avec badge numéroté"""
    c.setFillColor(BLUE)
    c.circle(MARGIN + 12, y + 6, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(MARGIN + 12, y + 2, str(number))
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN + 30, y, title)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.5)
    c.line(MARGIN + 30, y - 4, width - MARGIN, y - 4)
    return y - 22

def draw_wrapped_text(c, text, x, y, max_width, font_name="Helvetica", font_size=9.5, leading=12):
    c.setFont(font_name, font_size)
    line = ""
    for word in text.split():
        test = (line + " " + word).strip()
        if c.stringWidth(test, font_name, font_size) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

def draw_brand_grid(c, y, title, brands, accent):
    """Grille de logos de marques"""
    c.setFillColor(accent)
    c.roundRect(MARGIN, y - 24, CONTENT_W, 24, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, y - 16, title)
    y -= 32
    card_w = (CONTENT_W - (len(brands) - 1) * 8) / len(brands)
    card_h = 48
    for i, (slug, label) in enumerate(brands):
        cx = MARGIN + i * (card_w + 8)
        cy = y - card_h
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(cx, cy, card_w, card_h, 6, fill=1, stroke=0)
        c.setStrokeColor(accent)
        c.setLineWidth(1.2)
        c.roundRect(cx, cy, card_w, card_h, 6, fill=0, stroke=1)
        logo_path = LOGO_DIR + slug
        try:
            c.drawImage(ImageReader(logo_path), cx + 8, cy + 8,
                        width=card_w - 16, height=card_h - 16,
                        preserveAspectRatio=True, mask='auto')
        except:
            c.setFillColor(accent)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(cx + card_w / 2, cy + card_h / 2 - 5, label)
    return y - card_h - 20

# ----------------------------------------------------------------------
# PAGE 1 : COUVERTURE + DOMAINES
# ----------------------------------------------------------------------
c = canvas.Canvas(OUT, pagesize=A4)

# ========== HEADER AVEC IMAGE ==========
header_height = 150  # Hauteur du header en pixels
header_img_path = SRC + 'header.png'  # Chemin vers votre image d'en-tête

try:
    # Dessiner l'image en haut de page (pleine largeur)
    c.drawImage(ImageReader(header_img_path), 
                0, height - header_height, 
                width, header_height, 
                preserveAspectRatio=False, 
                mask='auto')
except:
    # Fallback si l'image n'existe pas : fond bleu avec texte
    c.setFillColor(BLUE)
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 45, "Eco Air Solutions")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 65, "Expertise CVC & Solutions Climatisation")

# ========== TITRE PRINCIPAL ==========
title_y = height - header_height - 60  # Position automatique sous le header

c.setFillColor(BLUE)
c.setFont("Helvetica-Bold", 32)
c.drawCentredString(width / 2, title_y, "OFFRE DE SERVICE")

c.setFillColor(DARK_GRAY)
c.setFont("Helvetica", 15)
c.drawCentredString(width / 2, title_y - 25, "Expertise CVC & Solutions Climatisation")

c.setFillColor(MID_GRAY)
c.setFont("Helvetica-Oblique", 11)
c.drawCentredString(width / 2, title_y - 45, "Avril 2026  •  Alger, Algérie")

# ========== LOGO ==========
logo_y = title_y - 50
logo_size = 50

# ========== DIVIDER ORANGE ==========
c.setStrokeColor(ORANGE)
c.setLineWidth(2)
c.line(MARGIN + 60, logo_y - 30, width - MARGIN - 60, logo_y - 30)

# ========== ENCADRÉ D'INTRODUCTION ==========
by = logo_y - 50
intro_box_h = 88
c.setFillColor(LIGHT_BLUE)
c.roundRect(MARGIN, by - intro_box_h, CONTENT_W, intro_box_h, 8, fill=1, stroke=0)
c.setStrokeColor(BLUE)
c.setLineWidth(2)
c.line(MARGIN, by - intro_box_h, MARGIN, by)

intro = ("Vous planifiez un projet CVC, une installation de climatisation, une ventilation "
         "technique ou une maintenance multi-sites ? Eco Air Solutions vous accompagne de "
         "l'étude jusqu'à la mise en service, avec des solutions adaptées aux contraintes "
         "de votre bâtiment, à votre budget et à vos exigences de performance énergétique. "
         "Nos équipes interviennent sur les 69 wilayas pour sécuriser vos délais, votre "
         "conformité et votre confort d'exploitation.")

c.setFillColor(DARK_GRAY)
draw_wrapped_text(c, intro, MARGIN + 15, by - 16, CONTENT_W - 30, "Helvetica", 9.5, 14)

# ========== 3 STATISTIQUES ==========
sy = by - intro_box_h - 30
for i, (num, label) in enumerate([("69", "Wilayas couvertes"), ("24/7", "Disponibilité SAV"), ("48h", "Devis garanti")]):
    bx = MARGIN + i * (CONTENT_W / 3) + (CONTENT_W / 6) - 40
    c.setFillColor(BLUE)
    c.roundRect(bx, sy - 50, 80, 55, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(bx + 40, sy - 22, num)
    c.setFont("Helvetica", 8)
    c.drawCentredString(bx + 40, sy - 36, label)

# ========== SECTION 1 : DOMAINES D'INTERVENTION ==========
y = sy - 94
y = draw_section_title(c, y, 1, "NOS DOMAINES D'INTERVENTION")
y -= 4

sector_intro = ("Une proposition pensée pour votre secteur : confort, conformité, performance "
                "et continuité d'exploitation.")
c.setFillColor(DARK_GRAY)
y = draw_wrapped_text(c, sector_intro, MARGIN, y, CONTENT_W, "Helvetica", 8.6, 11) - 4

sectors = [
    ('sector-building.jpg', 'Résidentiel', 'Confort durable pour villas et immeubles.'),
    ('sector-commercial.jpg', 'Tertiaire & Bureaux', 'Air stable pour équipes et visiteurs.'),
    ('sector-energy.jpg', 'Industrie & Énergie', "Continuité d'exploitation et sécurité."),
    ('sector-healthcare.jpg', 'Santé & Hospitalier', 'Air traité et conformité zones sensibles.'),
    ('sector-hospitality.jpg', 'Hôtellerie & Restauration', 'Confort client, cuisines et froid fiable.'),
    ('sector-food-industry.jpg', 'Agroalimentaire', 'Chaîne du froid et qualité produit.'),
]

card_w = (CONTENT_W - 20) / 3
card_h = 106
col_gap = 10
row_gap = 8
img_h = 56

for i, (img, title, desc) in enumerate(sectors):
    col = i % 3
    row = i // 3
    cx = MARGIN + col * (card_w + col_gap)
    cy = y - row * (card_h + row_gap)
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(cx, cy - card_h, card_w, card_h, 5, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(cx, cy - card_h, 5, card_h, 2, fill=1, stroke=0)
    try:
        c.drawImage(ImageReader(SRC + img), cx + 12, cy - img_h - 8,
                    width=card_w - 24, height=img_h, preserveAspectRatio=True, mask='auto')
    except:
        pass
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawCentredString(cx + card_w / 2, cy - img_h - 22, title)
    c.setFillColor(DARK_GRAY)
    c.setFont("Helvetica", 7.5)
    words = desc.split()
    line = ""
    dy = cy - img_h - 35
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 7.5) < card_w - 24:
            line = test
        else:
            c.drawCentredString(cx + card_w / 2, dy, line)
            dy -= 10
            line = w
    c.drawCentredString(cx + card_w / 2, dy, line)

c.showPage()   # fin page 1

# ----------------------------------------------------------------------
# PAGE 2 : SERVICES + ENGAGEMENTS
# ----------------------------------------------------------------------
y = height - 30
y = draw_section_title(c, y, 2, "NOS SERVICES")
y -= 12

service_intro = ("Pour faciliter votre lecture, notre offre est structurée autour de quatre "
                 "compétences clés, complétées par des lots techniques mobilisables selon "
                 "la nature du projet.")
c.setFillColor(DARK_GRAY)
y = draw_wrapped_text(c, service_intro, MARGIN, y, CONTENT_W, "Helvetica", 9.5, 13) - 6

c.setFillColor(BLUE)
c.setFont("Helvetica-Bold", 11)
c.drawString(MARGIN, y, "Compétences clés")
y -= 12

core_services = [
    ("01", "Étude & conception", [
        "Cadrage du besoin et choix des solutions techniques.",
        "Bilans thermiques, calculs de charges et dimensionnement.",
        "Plans CVC détaillés, audit et optimisation énergétique.",
    ]),
    ("02", "Installation CVC", [
        "VRF, Split, Multi-Split, cassette, gainable et centralisé.",
        "Sélection d'équipements fiables et basse consommation.",
        "Pose, raccordement, essais et mise en service contrôlée.",
    ]),
    ("03", "Ventilation & traitement d'air", [
        "VMC, CTA, double flux, extraction et renouvellement d'air.",
        "Filtration HEPA/ULPA selon les contraintes du site.",
        "Humidification, déshumidification et désenfumage.",
    ]),
    ("04", "Maintenance & SAV", [
        "Maintenance préventive et corrective des installations.",
        "Contrats adaptés aux sites résidentiels, tertiaires et industriels.",
        "Assistance 24h/24, 7j/7 pour les urgences techniques.",
    ]),
]

col_w = (CONTENT_W - 10) / 2
core_h = 86
row_gap = 8
for i, (num, title, items) in enumerate(core_services):
    col = i % 2
    row = i // 2
    bx = MARGIN + col * (col_w + 10)
    cy = y - row * (core_h + row_gap)
    c.setFillColor(LIGHT_BLUE)
    c.roundRect(bx, cy - core_h, col_w, core_h, 6, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(bx + 16, cy - 13, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(bx + 16, cy - 16, num)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(bx + 34, cy - 14, title)
    iy = cy - 31
    for item in items:
        c.setFillColor(ORANGE)
        c.circle(bx + 10, iy + 3, 2.2, fill=1, stroke=0)
        c.setFillColor(DARK_GRAY)
        iy = draw_wrapped_text(c, item, bx + 18, iy, col_w - 24, "Helvetica", 7.7, 9) - 1

core_rows = (len(core_services) + 1) // 2
y = y - core_rows * core_h - (core_rows - 1) * row_gap - 18

c.setFillColor(BLUE)
c.setFont("Helvetica-Bold", 11)
c.drawString(MARGIN, y, "Services complémentaires")
y -= 12

complementary_services = [
    ("Chauffage", "PAC, radiateurs, planchers chauffants, chaudières et eau chaude."),
    ("Froid industriel", "Chambres froides, entrepôts frigorifiques et réfrigération."),
    ("Protection incendie", "Détection, extinction automatique, sprinklage et sécurité incendie."),
    ("Électricité", "Tableaux, câblage, éclairage et mise en conformité."),
    ("Régulation GTB/GTC", "Supervision, domotique et gestion technique du bâtiment."),
    ("Pharmaceutique", "Salles blanches, HVAC pharmaceutique et contrôle température/hygrométrie."),
    ("Fluides médicaux", "Réseaux O2, vide médical, air comprimé et conformité hospitalière."),
    ("Désenfumage", "Désenfumage mécanique/naturel et extraction fumées/chaleur."),
    ("Audit énergétique", "Optimisation des consommations et réduction des coûts d'exploitation."),
]

comp_h = 40
comp_gap = 5
for i, (title, desc) in enumerate(complementary_services):
    col = i % 2
    row = i // 2
    bx = MARGIN + col * (col_w + 10)
    by = y - row * (comp_h + comp_gap)
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(bx, by - comp_h, col_w, comp_h, 5, fill=1, stroke=0)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.line(bx, by, bx, by - comp_h)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(bx + 10, by - 12, title)
    c.setFillColor(DARK_GRAY)
    draw_wrapped_text(c, desc, bx + 10, by - 25, col_w - 18, "Helvetica", 7.3, 8)

comp_rows = (len(complementary_services) + 1) // 2
y_after_services = y - comp_rows * comp_h - (comp_rows - 1) * comp_gap - 24

# --- SECTION 3 : ENGAGEMENTS (juste après les services) ---
y = y_after_services
y = draw_section_title(c, y, 3, "NOS ENGAGEMENTS")
y -= 15 

engagements = [
    ("Réactivité", "Diagnostic et devis sous 48h après réception de votre demande."),
    ("Couverture nationale", "Intervention sur les 69 wilayas d'Algérie avec équipes locales."),
    ("Conformité", "Respect strict des normes algériennes (DTR) et internationales (ISO, EN)."),
    ("Éco-responsabilité", "Optimisation énergétique pour réduire vos coûts d'exploitation."),
]

eng_col_w = (CONTENT_W - 10) / 2
eng_row_h = 75
for i, (title, desc) in enumerate(engagements):
    col = i % 2
    row = i // 2
    bx = MARGIN + col * (eng_col_w + 10)
    by = y - row * eng_row_h
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(bx, by - 68, eng_col_w, 68, 6, fill=1, stroke=0)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.line(bx, by, bx, by - 68)
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(bx + 12, by - 18, title)
    c.setFillColor(DARK_GRAY)
    c.setFont("Helvetica", 9.5)
    words = desc.split()
    line = ""
    dy = by - 33
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 9.5) < eng_col_w - 20:
            line = test
        else:
            c.drawString(bx + 12, dy, line)
            dy -= 13
            line = w
    c.drawString(bx + 12, dy, line)

c.showPage()   # fin page 2

# ----------------------------------------------------------------------
# PAGE 3 : MARQUES + CONTACT
# ----------------------------------------------------------------------
y = height - 30
y = draw_section_title(c, y, 4, "NOS MARQUES PARTENAIRES")
y -= 15

# Grille climatisation
clim_brands = [
    ("samsung-logo.png", "Samsung"),
    ("lg-logo.png", "LG"),
    ("condor-logo.png", "Condor"),
    ("trane-logo.png", "Trane"),
    ("ciat-logo.png", "CIAT"),
]
y = draw_brand_grid(c, y, "CLIMATISATION  —  Systèmes split, VRF & centralisés", clim_brands, BLUE)
y -= 8

# --- Grille Ventilation & Aération ---
ventilation_brands = [
    ("fa-logo.png", "France Air"),
    ("systemair-logo.png", "Systemair"),
]

y = draw_brand_grid(c, y, "VENTILATION & AÉRATION  —  CTA, VMC & extraction", ventilation_brands, BLUE)
y -= 8

# --- Grille Détection Incendie ---
detection_brands = [
    ("def-logo.png", "DEF"),
    ("abb-logo.png", "ABB"),
]
y = draw_brand_grid(c, y, "DÉTECTION INCENDIE  —  SSI, centrales & détecteurs", detection_brands, ORANGE)
y -= 8


# Grille désenfumage
desenfumage_brands = [("dynair-logo.png", "Dynair")]
y = draw_brand_grid(c, y, "DÉSENFUMAGE  —  Ventilation & extraction incendie", desenfumage_brands, ORANGE)
y -= 10


# --- Grille Électricité (NOUVELLE SECTION) ---
electricite_brands = [
    ("se-logo.png", "Schneider Electric"),
]

y = draw_brand_grid(c, y, "ÉLECTRICITÉ  —  Matériel électrique, tableaux & armoires", electricite_brands, BLUE)
y -= 8

# Note partenariats
c.setFillColor(LIGHT_BLUE)
c.roundRect(MARGIN, y - 50, CONTENT_W, 50, 6, fill=1, stroke=0)
c.setStrokeColor(BLUE)
c.setLineWidth(1)
c.roundRect(MARGIN, y - 50, CONTENT_W, 50, 6, fill=0, stroke=1)
c.setFillColor(BLUE)
c.setFont("Helvetica-Bold", 10)
c.drawString(MARGIN + 14, y - 16, "Partenariats officiels & approvisionnement garanti")
c.setFillColor(DARK_GRAY)
c.setFont("Helvetica", 9.5)
c.drawString(MARGIN + 14, y - 30, "Eco Air Solutions travaille en partenariat direct avec ces fabricants pour garantir")
c.drawString(MARGIN + 14, y - 43, "l'approvisionnement en pièces détachées, la garantie constructeur et le support technique.")

# --- CARTE DE CONTACT ---
card_h = 130
y_contact = y - 60
c.setFillColor(BLUE)
c.roundRect(MARGIN, y_contact - card_h, CONTENT_W, card_h, 8, fill=1, stroke=0)
try:
    c.drawImage(ImageReader(SRC + 'logo-square.png'), MARGIN + 15, y_contact - card_h + 15,
                width=100, height=100, preserveAspectRatio=True, mask='auto')
except:
    pass
c.setFillColor(white)
c.setFont("Helvetica-Bold", 14)
c.drawString(MARGIN + 130, y_contact - 25, "Eco Air Solutions")
c.setFont("Helvetica", 10)
contacts = [
    "Demandez votre diagnostic et devis gratuit sous 48h.",
    "Bureau Alger : Cités Vertes, Ouled Fayet, Alger, 16000",
    "Antenne Mila : Rue Boutaf Boulaid, Zeghaia, Mila, 43012",
    "+213 (0) 799 967 458",
    "ecoairsolutions909@gmail.com",
    "https://eco-air-solutions.github.io/",
]
cy = y_contact - 45
for ct in contacts:
    c.drawString(MARGIN + 130, cy, ct)
    cy -= 15

c.save()
print("PDF généré avec succès :", OUT)
