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

def draw_brand_grid(c, y, title, brands, accent):
    """Grille de logos de marques"""
    c.setFillColor(accent)
    c.roundRect(MARGIN, y - 24, CONTENT_W, 24, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2, y - 16, title)
    y -= 32
    card_w = (CONTENT_W - (len(brands) - 1) * 8) / len(brands)
    card_h = 54
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

# ========== ENCADRÉ "QUI SOMMES-NOUS" ==========
by = logo_y - 50
c.setFillColor(LIGHT_BLUE)
c.roundRect(MARGIN, by - 90, CONTENT_W, 90, 8, fill=1, stroke=0)
c.setStrokeColor(BLUE)
c.setLineWidth(2)
c.line(MARGIN, by - 90, MARGIN, by)

intro = ("Eco Air Solutions est une entreprise specialisee dans l'etude, l'installation et la "
         "maintenance de systemes CVC (Chauffage, Ventilation, Climatisation) en Algerie. "
         "Nous accompagnons les professionnels et les particuliers avec une approche "
         "ecoresponsable, privilegiant les solutions a basse consommation energetique. "
         "Forts d'une presence sur les 69 wilayas, nous garantissons une expertise de "
         "proximite sur tout le territoire national.")

c.setFillColor(DARK_GRAY)
c.setFont("Helvetica", 10)
text_obj = c.beginText(MARGIN + 15, by - 15)
text_obj.setLeading(15)
words = intro.split()
line = ""
for w in words:
    test = (line + " " + w).strip()
    if c.stringWidth(test, "Helvetica", 10) < CONTENT_W - 30:
        line = test
    else:
        text_obj.textLine(line)
        line = w
text_obj.textLine(line)
c.drawText(text_obj)

# ========== 3 STATISTIQUES ==========
sy = by - 120
for i, (num, label) in enumerate([("69", "Wilayas couvertes"), ("24/7", "Disponibilite SAV"), ("48h", "Devis garanti")]):
    bx = MARGIN + i * (CONTENT_W / 3) + (CONTENT_W / 6) - 40
    c.setFillColor(BLUE)
    c.roundRect(bx, sy - 50, 80, 55, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(bx + 40, sy - 22, num)
    c.setFont("Helvetica", 8)
    c.drawCentredString(bx + 40, sy - 36, label)

# ========== SECTION 1 : DOMAINES D'INTERVENTION ==========
y = sy - 120
y = draw_section_title(c, y, 1, "NOS DOMAINES D'INTERVENTION")
y -= 10

sectors = [
    ('sector-building.jpg', 'Residentiel', 'Villas, appartements et habitations collectives.'),
    ('sector-commercial.jpg', 'Tertiaire & Bureaux', 'Centres commerciaux et espaces de travail.'),
    ('sector-energy.jpg', 'Industrie & Energie', 'Usines, entrepots et centrales electriques.'),
    ('sector-healthcare.jpg', 'Sante & Hospitalier', 'Hopitaux, laboratoires, filtration HEPA.'),
    ('sector-hospitality.jpg', 'Hotellerie & Restauration', 'Solutions silencieuses et performantes.'),
    ('sector-food-industry.jpg', 'Agroalimentaire', 'Chambres froides et controle hygrometrie.'),
]

card_w = (CONTENT_W - 10) / 2
card_h = 62
col_gap = 10
img_w = 55

for i, (img, title, desc) in enumerate(sectors):
    col = i % 2
    row = i // 2
    cx = MARGIN + col * (card_w + col_gap)
    cy = y - row * (card_h + 8)
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(cx, cy - card_h, card_w, card_h, 5, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(cx, cy - card_h, 5, card_h, 2, fill=1, stroke=0)
    try:
        c.drawImage(ImageReader(SRC + img), cx + 8, cy - card_h + 6,
                    width=img_w, height=card_h - 12, preserveAspectRatio=True, mask='auto')
    except:
        pass
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(cx + img_w + 14, cy - 18, title)
    c.setFillColor(DARK_GRAY)
    c.setFont("Helvetica", 8.5)
    words = desc.split()
    line = ""
    dy = cy - 30
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 8.5) < card_w - img_w - 20:
            line = test
        else:
            c.drawString(cx + img_w + 14, dy, line)
            dy -= 12
            line = w
    c.drawString(cx + img_w + 14, dy, line)

c.showPage()   # fin page 1

# ----------------------------------------------------------------------
# PAGE 2 : SERVICES + ENGAGEMENTS
# ----------------------------------------------------------------------
y = height - 30
y = draw_section_title(c, y, 2, "NOS SERVICES")
y -= 12

services_list = [
    {"letter": "A", "title": "Etude & Conception", "items": ["Bilans thermiques et calculs de charges.", "Plans CVC detailles (BIM/CAD).", "Audit et optimisation energetique."]},
    {"letter": "B", "title": "Climatisation", "items": ["Systemes VRF, Split, Multi-Split.", "Cassette, gainable et centralise.", "Solutions inverter haute efficacite."]},
    {"letter": "C", "title": "Ventilation", "items": ["VMC et ventilation mecanique.", "CTA et double flux.", "Desenfumage."]},
    {"letter": "D", "title": "Traitement de l'Air", "items": ["CTA et unites de traitement.", "Filtration HEPA, ULPA.", "Humidification et deshumidification."]},
    {"letter": "E", "title": "Chauffage", "items": ["Pompes a chaleur (PAC).", "Radiateurs et planchers chauffants.", "Production eau chaude et chaudieres."]},
    {"letter": "F", "title": "Froid Industriel", "items": ["Chambres froides et caves a vin.", "Entrepots frigorifiques.", "Systemes de refrigeration."]},
    {"letter": "G", "title": "Desenfumage", "items": ["Desenfumage mecanique et naturel.", "Extraction fumees et chaleur.", "Ventilation de securite (SEC)."]},
    {"letter": "H", "title": "Protection Incendie", "items": ["Detection incendie (DET).", "Extinction automatique.", "Sprinklage et desenfumage."]},
    {"letter": "I", "title": "Detection Incendie", "items": ["Detecteurs fumees et chaleur.", "Centrales dalarme (SSI).", "Transmission BAAS et PC securite."]},
    {"letter": "J", "title": "Electricite", "items": ["Installation electrique.", "Tableaux et cablage.", "Eclairage et mise a la norme."]},
    {"letter": "K", "title": "Regulation", "items": ["Systemes GTB/GTC.", "Supervision et domotique.", "Gestion technique du batiment."]},
    {"letter": "L", "title": "Pharmaceutique", "items": ["Salles blanches.", "HVAC pharmaceutique et PCR.", "Controle temperature/hygrometrie."]},
    {"letter": "M", "title": "Fluides Medicaux", "items": ["Reseaux O2 et vide medical.", "Air comprime medical.", "Conformite normes hospitalieres."]},
    {"letter": "N", "title": "Maintenance & SAV", "items": ["Maintenance preventive et corrective.", "Disponibilite 24h/24, 7j/7.", "Mise en service et formation."]},
]

col_w = (CONTENT_W - 10) / 2
bh = 65          # hauteur réduite pour tenir sur la page
row_gap = 6
for i, svc in enumerate(services_list):
    col = i % 2
    row = i // 2
    bx = MARGIN + col * (col_w + 10)
    cy = y - row * (bh + row_gap)
    c.setFillColor(LIGHT_BLUE)
    c.roundRect(bx, cy - bh, col_w, bh, 6, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.circle(bx + 16, cy - 12, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(bx + 16, cy - 16, svc["letter"])
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(bx + 32, cy - 14, svc["title"])
    iy = cy - 32
    for item in svc["items"]:
        c.setFillColor(ORANGE)
        c.circle(bx + 10, iy + 3, 2.5, fill=1, stroke=0)
        c.setFillColor(DARK_GRAY)
        c.setFont("Helvetica", 8.5)
        words = item.split()
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 8.5) < col_w - 22:
                line = test
            else:
                c.drawString(bx + 18, iy, line)
                iy -= 11
                line = w
        c.drawString(bx + 18, iy, line)
        iy -= 12   # espacement entre items réduit

y_after_services = y - ((len(services_list)+1)//2) * (bh + row_gap) - 30

# --- SECTION 3 : ENGAGEMENTS (juste après les services) ---
y = y_after_services
y = draw_section_title(c, y, 3, "NOS ENGAGEMENTS")
y -= 15 

engagements = [
    ("Reactivite", "Diagnostic et devis sous 48h apres reception de votre demande.", "⏱"),
    ("Couverture Nationale", "Intervention sur les 69 wilayas d'Algerie avec equipes locales.", "🗺"),
    ("Conformite", "Respect strict des normes algeriennes (DTR) et internationales (ISO, EN).", "✅"),
    ("Eco-responsabilite", "Optimisation energetique pour reduire vos couts d'exploitation.", "🌿"),
]

eng_col_w = (CONTENT_W - 10) / 2
eng_row_h = 75
for i, (title, desc, icon) in enumerate(engagements):
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
y -= 18

# --- Grille Ventilation & Aération ---
ventilation_brands = [
    ("fa-logo.png", "France Air"),
    ("systemair-logo.png", "Systemair"),
]

y = draw_brand_grid(c, y, "VENTILATION & AÉRATION  —  CTA, VMC & extraction", ventilation_brands, BLUE)
y -= 18

# --- Grille Détection Incendie ---
detection_brands = [
    ("def-logo.png", "DEF"),
    ("abb-logo.png", "ABB"),
]
y = draw_brand_grid(c, y, "DÉTECTION INCENDIE  —  SSI, centrales & détecteurs", detection_brands, ORANGE)
y -= 18


# Grille désenfumage
desenfumage_brands = [("dynair-logo.png", "Dynair")]
y = draw_brand_grid(c, y, "DÉSENFUMAGE  —  Ventilation & extraction incendie", desenfumage_brands, ORANGE)
y -= 25


# --- Grille Électricité (NOUVELLE SECTION) ---
electricite_brands = [
    ("se-logo.png", "Schneider Electric"),
]

y = draw_brand_grid(c, y, "ÉLECTRICITÉ  —  Matériel électrique, tableaux & armoires", electricite_brands, BLUE)
y -= 18

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
y_contact = height - 680   
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
    "Cites Vertes, Ouled Fayet, Alger, 16000",
    "Rue Boutaf Boulaid, Zeghaia, Mila, 43012",
    "+213 (0) 799 967 458",
    "ecoairsolutions909@gmail.com",
    "https://eco-air-solutions.github.io/",
]
cy = y_contact - 45
for ct in contacts:
    c.drawString(MARGIN + 130, cy, ct)
    cy -= 16

c.save()
print("PDF généré avec succès :", OUT)
