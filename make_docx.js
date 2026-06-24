const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  ImageRun,
  Header,
  Footer,
  AlignmentType,
  LevelFormat,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  PageBreak,
  PageNumber,
} = require("docx");
const fs = require("fs");
const path = require("path");

const SRC = "";
const OUT = "offre_service_eco_air.docx";

const BLUE = "005EA4";
const ORANGE = "E8520A";
const LIGHT_BLUE = "DCF0FF";
const WHITE = "FFFFFF";
const DARK_GRAY = "333333";
const LIGHT_GRAY = "F2F2F2";
const MID_GRAY = "666666";

const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = {
  top: NO_BORDER,
  bottom: NO_BORDER,
  left: NO_BORDER,
  right: NO_BORDER,
  insideH: NO_BORDER,
  insideV: NO_BORDER,
};

function loadImg(name, w, h) {
  const p = path.join(SRC, name);
  if (!fs.existsSync(p)) return null;
  const data = fs.readFileSync(p);
  const ext = name.split(".").pop().toLowerCase();
  return new ImageRun({
    data,
    transformation: { width: w, height: h },
    type: ext === "jpg" ? "jpg" : "png",
    altText: { title: name, description: name, name },
  });
}

function spacer(pt = 100) {
  return new Paragraph({
    children: [new TextRun({ text: "" })],
    spacing: { before: 0, after: pt },
  });
}

function sectionHeading(text) {
  return new Paragraph({
    children: [
      new TextRun({ text, bold: true, size: 28, color: BLUE, font: "Arial" }),
    ],
    spacing: { before: 280, after: 140 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: BLUE, space: 4 },
    },
  });
}

// PAGE 1 ─────────────────────────────────────────────────────────────────────

function coverTitleTable() {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: noBorders,
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: BLUE, type: ShadingType.CLEAR },
            margins: { top: 320, bottom: 320, left: 400, right: 400 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "OFFRE DE SERVICE",
                    bold: true,
                    size: 56,
                    color: WHITE,
                    font: "Arial",
                  }),
                ],
                alignment: AlignmentType.CENTER,
              }),
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Expertise CVC & Solutions Climatisation",
                    size: 28,
                    color: "CCE8FF",
                    font: "Arial",
                  }),
                ],
                alignment: AlignmentType.CENTER,
                spacing: { before: 60, after: 60 },
              }),
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Avril 2026  \u2022  Alger, Algérie",
                    size: 18,
                    color: "AACCEE",
                    font: "Arial",
                    italics: true,
                  }),
                ],
                alignment: AlignmentType.CENTER,
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function logoTaglineTable() {
  const logoImg = loadImg("logo.png", 110, 110);
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2000, 7360],
    borders: noBorders,
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 2000, type: WidthType.DXA },
            margins: { top: 100, bottom: 100, left: 100, right: 200 },
            verticalAlign: VerticalAlign.CENTER,
            children: logoImg
              ? [
                  new Paragraph({
                    children: [logoImg],
                    alignment: AlignmentType.CENTER,
                  }),
                ]
              : [new Paragraph({ children: [] })],
          }),
          new TableCell({
            width: { size: 7360, type: WidthType.DXA },
            margins: { top: 100, bottom: 100, left: 200, right: 100 },
            verticalAlign: VerticalAlign.CENTER,
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "L\u2019expertise au service de votre confort durable.",
                    bold: true,
                    size: 30,
                    color: BLUE,
                    font: "Arial",
                    italics: true,
                  }),
                ],
                spacing: { after: 80 },
              }),
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Technique  \u2022  Esthétique  \u2022  Confort",
                    size: 18,
                    color: MID_GRAY,
                    font: "Arial",
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function introPara() {
  return new Paragraph({
    border: {
      left: { style: BorderStyle.SINGLE, size: 16, color: BLUE, space: 10 },
    },
    indent: { left: 260 },
    shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
    children: [
      new TextRun({
        text: "Vous planifiez un projet CVC, une installation de climatisation, une ventilation technique ou une maintenance multi-sites ? Eco Air Solutions vous accompagne de l'étude jusqu'à la mise en service, avec des solutions adaptées aux contraintes de votre bâtiment, à votre budget et à vos exigences de performance énergétique. Nos équipes interviennent sur les 69 wilayas pour sécuriser vos délais, votre conformité et votre confort d'exploitation.",
        size: 20,
        color: DARK_GRAY,
        font: "Arial",
      }),
    ],
    spacing: { before: 60, after: 100 },
  });
}

function statsTable() {
  const stats = [
    ["69", "Wilayas couvertes"],
    ["24/7", "Disponibilite SAV"],
    ["48h", "Devis garanti"],
  ];
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3000, 3000, 3360],
    borders: noBorders,
    rows: [
      new TableRow({
        children: stats.map(
          ([num, lbl], i) =>
            new TableCell({
              width: { size: i < 2 ? 3000 : 3360, type: WidthType.DXA },
              shading: { fill: BLUE, type: ShadingType.CLEAR },
              margins: { top: 160, bottom: 160, left: 100, right: 100 },
              verticalAlign: VerticalAlign.CENTER,
              children: [
                new Paragraph({
                  children: [
                    new TextRun({
                      text: num,
                      bold: true,
                      size: 52,
                      color: WHITE,
                      font: "Arial",
                    }),
                  ],
                  alignment: AlignmentType.CENTER,
                }),
                new Paragraph({
                  children: [
                    new TextRun({
                      text: lbl,
                      size: 16,
                      color: "CCE8FF",
                      font: "Arial",
                    }),
                  ],
                  alignment: AlignmentType.CENTER,
                }),
              ],
            }),
        ),
      }),
    ],
  });
}

// SECTORS (Domaine d'intervention) ──────────────────────────────────────────

const sectors = [
  [
    "sector-building.jpg",
    "Résidentiel",
    "Confort durable pour villas, résidences et immeubles collectifs.",
  ],
  [
    "sector-commercial.jpg",
    "Tertiaire & Bureaux",
    "Air stable, silencieux et maîtrisé pour vos équipes et visiteurs.",
  ],
  [
    "sector-energy.jpg",
    "Industrie & Énergie",
    "Installations robustes pour continuité d'exploitation et sécurité.",
  ],
  [
    "sector-healthcare.jpg",
    "Santé & Hospitalier",
    "Air traité, filtration et conformité pour zones sensibles.",
  ],
  [
    "sector-hospitality.jpg",
    "Hôtellerie & Restauration",
    "Confort client, cuisines ventilées et froid fiable au quotidien.",
  ],
  [
    "sector-food-industry.jpg",
    "Agroalimentaire",
    "Chaîne du froid, hygrométrie et qualité produit sécurisées.",
  ],
];

function sectorIntroPara() {
  return new Paragraph({
    children: [
      new TextRun({
        text: "Une proposition pensée pour votre secteur : confort, conformité, performance et continuité d'exploitation.",
        size: 18,
        color: DARK_GRAY,
        font: "Arial",
      }),
    ],
    alignment: AlignmentType.CENTER,
    spacing: { after: 20 },
  });
}

function sectorCard(imgFile, title, desc, accentColor) {
  const si = loadImg(imgFile, 136, 84);
  return new TableCell({
    width: { size: 3000, type: WidthType.DXA },
    shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: "E4E4E4" },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: "E4E4E4" },
      right: { style: BorderStyle.SINGLE, size: 2, color: "E4E4E4" },
      left: { style: BorderStyle.SINGLE, size: 10, color: accentColor },
    },
    margins: { top: 100, bottom: 100, left: 110, right: 110 },
    verticalAlign: VerticalAlign.TOP,
    children: [
      new Paragraph({
        children: si ? [si] : [],
        alignment: AlignmentType.CENTER,
        spacing: { after: 80 },
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: title,
            bold: true,
            size: 19,
            color: BLUE,
            font: "Arial",
          }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 45 },
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: desc,
            size: 15,
            color: DARK_GRAY,
            font: "Arial",
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
    ],
  });
}

function sectorsGrid() {
  const gapCell = () =>
    new TableCell({
      width: { size: 180, type: WidthType.DXA },
      borders: noBorders,
      children: [new Paragraph({ children: [] })],
    });
  const rows = [];
  for (let i = 0; i < sectors.length; i += 3) {
    rows.push(
      new TableRow({
        children: [
          sectorCard(...sectors[i], BLUE),
          gapCell(),
          sectorCard(...sectors[i + 1], ORANGE),
          gapCell(),
          sectorCard(...sectors[i + 2], BLUE),
        ],
      }),
    );
    if (i + 3 < sectors.length) {
      rows.push(
        new TableRow({
          children: [
            new TableCell({
              width: { size: 3000, type: WidthType.DXA },
              borders: noBorders,
              children: [new Paragraph({ children: [], spacing: { after: 90 } })],
            }),
            gapCell(),
            new TableCell({
              width: { size: 3000, type: WidthType.DXA },
              borders: noBorders,
              children: [new Paragraph({ children: [] })],
            }),
            gapCell(),
            new TableCell({
              width: { size: 3000, type: WidthType.DXA },
              borders: noBorders,
              children: [new Paragraph({ children: [] })],
            }),
          ],
        }),
      );
    }
  }
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [3000, 180, 3000, 180, 3000],
    borders: noBorders,
    rows,
  });
}

// SERVICES ──────────────────────────────────────────────────────────────────

const coreServices = [
  {
    kicker: "01",
    title: "Étude & conception",
    items: [
      "Cadrage du besoin et choix des solutions techniques.",
      "Bilans thermiques, calculs de charges et dimensionnement.",
      "Plans CVC détaillés, audit et optimisation énergétique.",
    ],
  },
  {
    kicker: "02",
    title: "Installation CVC",
    items: [
      "VRF, Split, Multi-Split, cassette, gainable et centralisé.",
      "Sélection d'équipements fiables et basse consommation.",
      "Pose, raccordement, essais et mise en service contrôlée.",
    ],
  },
  {
    kicker: "03",
    title: "Ventilation & traitement d'air",
    items: [
      "VMC, CTA, double flux, extraction et renouvellement d'air.",
      "Filtration HEPA/ULPA selon les contraintes du site.",
      "Humidification, déshumidification et désenfumage.",
    ],
  },
  {
    kicker: "04",
    title: "Maintenance & SAV",
    items: [
      "Maintenance préventive et corrective des installations.",
      "Contrats adaptés aux sites résidentiels, tertiaires et industriels.",
      "Assistance 24h/24, 7j/7 pour les urgences techniques.",
    ],
  },
];

const complementaryServices = [
  ["Chauffage", "PAC, radiateurs, planchers chauffants, chaudières et eau chaude."],
  ["Froid industriel", "Chambres froides, entrepôts frigorifiques et réfrigération."],
  ["Protection incendie", "Détection, extinction automatique, sprinklage et sécurité incendie."],
  ["Électricité", "Tableaux, câblage, éclairage et mise en conformité."],
  ["Régulation GTB/GTC", "Supervision, domotique et gestion technique du bâtiment."],
  ["Pharmaceutique", "Salles blanches, HVAC pharmaceutique et contrôle température/hygrométrie."],
  ["Fluides médicaux", "Réseaux O2, vide médical, air comprimé et conformité hospitalière."],
  ["Désenfumage", "Désenfumage mécanique/naturel et extraction fumées/chaleur."],
  ["Audit énergétique", "Optimisation des consommations et réduction des coûts d'exploitation."],
];

function serviceGroupTitle(text) {
  return new Paragraph({
    children: [
      new TextRun({ text, bold: true, size: 22, color: BLUE, font: "Arial" }),
    ],
    spacing: { before: 60, after: 80 },
  });
}

function coreServiceCard(svc, colWidth) {
  const bulletStyle = { size: 14, color: DARK_GRAY, font: "Arial" };
  return new TableCell({
    width: { size: colWidth, type: WidthType.DXA },
    shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
    borders: noBorders,
    margins: { top: 40, bottom: 40, left: 40, right: 40 },
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: svc.kicker,
            bold: true,
            size: 24,
            color: ORANGE,
            font: "Arial",
          }),
        ],
        spacing: { after: 40 },
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: svc.title,
            bold: true,
            size: 18,
            color: BLUE,
            font: "Arial",
          }),
        ],
        spacing: { after: 100 },
      }),
      ...svc.items.map(
        (item) =>
          new Paragraph({
            children: [new TextRun({ text: "• " + item, ...bulletStyle })],
            spacing: { after: 60 },
          }),
      ),
    ],
  });
}

function coreServicesTable() {
  const colWidth = 4440;
  const gapWidth = 480;
  const rows = [];
  const leftCol = coreServices.slice(0, 2);
  const rightCol = coreServices.slice(2);
  const maxRows = 2;
  for (let i = 0; i < maxRows; i++) {
    const leftCell =
      i < leftCol.length
        ? coreServiceCard(leftCol[i], colWidth)
        : new TableCell({
            width: { size: colWidth, type: WidthType.DXA },
            borders: noBorders,
            children: [new Paragraph({ children: [] })],
          });
    const rightCell =
      i < rightCol.length
        ? coreServiceCard(rightCol[i], colWidth)
        : new TableCell({
            width: { size: colWidth, type: WidthType.DXA },
            borders: noBorders,
            children: [new Paragraph({ children: [] })],
          });
    const gapCell = new TableCell({
      width: { size: gapWidth, type: WidthType.DXA },
      borders: noBorders,
      children: [new Paragraph({ children: [] })],
    });
    rows.push(new TableRow({ children: [leftCell, gapCell, rightCell] }));
    // add small spacing after each row except last
    if (i < maxRows - 1) {
      rows.push(
        new TableRow({
          children: [
            new TableCell({
              width: { size: 9360, type: WidthType.DXA },
              borders: noBorders,
              children: [
                new Paragraph({ children: [], spacing: { after: 60 } }),
              ],
            }),
          ],
        }),
      );
    }
  }
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [colWidth, gapWidth, colWidth],
    borders: noBorders,
    rows,
  });
}

function complementaryServiceCell([title, desc], colWidth) {
  return new TableCell({
    width: { size: colWidth, type: WidthType.DXA },
    shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
    borders: noBorders,
    margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: title, bold: true, size: 17, color: BLUE, font: "Arial" }),
        ],
        spacing: { after: 35 },
      }),
      new Paragraph({
        children: [new TextRun({ text: desc, size: 14, color: DARK_GRAY, font: "Arial" })],
      }),
    ],
  });
}

function complementaryServicesTable() {
  const colWidth = 4440;
  const gapWidth = 480;
  const rows = [];
  for (let i = 0; i < complementaryServices.length; i += 2) {
    const right = complementaryServices[i + 1];
    rows.push(
      new TableRow({
        children: [
          complementaryServiceCell(complementaryServices[i], colWidth),
          new TableCell({
            width: { size: gapWidth, type: WidthType.DXA },
            borders: noBorders,
            children: [new Paragraph({ children: [] })],
          }),
          right
            ? complementaryServiceCell(right, colWidth)
            : new TableCell({
                width: { size: colWidth, type: WidthType.DXA },
                borders: noBorders,
                children: [new Paragraph({ children: [] })],
              }),
        ],
      }),
    );
    if (i + 2 < complementaryServices.length) {
      rows.push(
        new TableRow({
          children: [
            new TableCell({
              width: { size: 9360, type: WidthType.DXA },
              borders: noBorders,
              children: [new Paragraph({ children: [], spacing: { after: 40 } })],
            }),
          ],
        }),
      );
    }
  }
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [colWidth, gapWidth, colWidth],
    borders: noBorders,
    rows,
  });
}

function servicesBlock() {
  return [
    serviceGroupTitle("Compétences clés"),
    coreServicesTable(),
    spacer(70),
    serviceGroupTitle("Services complémentaires"),
    complementaryServicesTable(),
  ];
}

// ENGAGEMENTS ────────────────────────────────────────────────────────────────

const engagementsList = [
  [
    "Réactivité",
    "Diagnostic et devis sous 48h après réception de votre demande.",
  ],
  [
    "Couverture nationale",
    "Intervention sur les 69 wilayas d'Algérie avec équipes locales.",
  ],
  [
    "Conformité",
    "Respect strict des normes algériennes (DTR) et internationales (ISO, EN).",
  ],
  [
    "Éco-responsabilité",
    "Optimisation énergétique pour réduire vos coûts d'exploitation.",
  ],
];

function makeEngCell([title, desc]) {
  return new TableCell({
    width: { size: 4440, type: WidthType.DXA },
    shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
    borders: {
      top: NO_BORDER,
      bottom: NO_BORDER,
      right: NO_BORDER,
      insideV: NO_BORDER,
      left: { style: BorderStyle.SINGLE, size: 12, color: BLUE },
    },
    margins: { top: 120, bottom: 120, left: 180, right: 120 },
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text: title,
            bold: true,
            size: 22,
            color: BLUE,
            font: "Arial",
          }),
        ],
        spacing: { after: 60 },
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: desc,
            size: 18,
            color: DARK_GRAY,
            font: "Arial",
          }),
        ],
      }),
    ],
  });
}

function engagementsTable() {
  const gapCol = new TableCell({
    width: { size: 480, type: WidthType.DXA },
    borders: noBorders,
    children: [new Paragraph({ children: [] })],
  });
  const rows = [];
  for (let i = 0; i < engagementsList.length; i += 2) {
    rows.push(
      new TableRow({
        children: [
          makeEngCell(engagementsList[i]),
          gapCol,
          makeEngCell(engagementsList[i + 1] || ["", ""]),
        ],
      }),
    );
    rows.push(
      new TableRow({
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            borders: noBorders,
            children: [new Paragraph({ children: [], spacing: { after: 80 } })],
          }),
        ],
      }),
    );
  }
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [4440, 480, 4440],
    borders: noBorders,
    rows,
  });
}

// BRAND SECTIONS (marques partenaires) ──────────────────────────────────────

function brandSectionHeader(title, accentColor) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: noBorders,
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: accentColor, type: ShadingType.CLEAR },
            margins: { top: 100, bottom: 100, left: 200, right: 200 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: title,
                    bold: true,
                    size: 22,
                    color: WHITE,
                    font: "Arial",
                  }),
                ],
                alignment: AlignmentType.CENTER,
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function brandLogoCell(slug, label, accentColor, colW) {
  const logoPath = path.join(LOGO_DIR, slug);
  let logoImg = null;
  if (fs.existsSync(logoPath)) {
    logoImg = new ImageRun({
      data: fs.readFileSync(logoPath),
      transformation: { width: colW > 1000 ? 120 : 90, height: 42 },
      type: "png",
      altText: { title: label, description: label, name: label },
    });
  }
  return new TableCell({
    width: { size: colW, type: WidthType.DXA },
    shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: accentColor },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: accentColor },
      left: { style: BorderStyle.SINGLE, size: 4, color: accentColor },
      right: { style: BorderStyle.SINGLE, size: 4, color: accentColor },
      insideH: NO_BORDER,
      insideV: NO_BORDER,
    },
    margins: { top: 80, bottom: 80, left: 80, right: 80 },
    verticalAlign: VerticalAlign.CENTER,
    children: logoImg
      ? [
          new Paragraph({
            children: [logoImg],
            alignment: AlignmentType.CENTER,
          }),
        ]
      : [
          new Paragraph({
            children: [
              new TextRun({
                text: label,
                bold: true,
                size: 20,
                color: accentColor,
                font: "Arial",
              }),
            ],
            alignment: AlignmentType.CENTER,
          }),
        ],
  });
}

function brandGrid(brands, accentColor) {
  const n = brands.length;
  const gap = 80;
  const totalGap = gap * (n - 1);
  const cellW = Math.floor((9360 - totalGap) / n);
  const lastW = 9360 - totalGap - cellW * (n - 1);
  const colWidths = brands.map((_, i) => (i < n - 1 ? cellW : lastW));
  const allWidths = [];
  brands.forEach((_, i) => {
    allWidths.push(colWidths[i]);
    if (i < n - 1) allWidths.push(gap);
  });

  const cells = [];
  brands.forEach(([slug, label], i) => {
    cells.push(brandLogoCell(slug, label, accentColor, colWidths[i]));
    if (i < n - 1)
      cells.push(
        new TableCell({
          width: { size: gap, type: WidthType.DXA },
          borders: noBorders,
          children: [new Paragraph({ children: [] })],
        }),
      );
  });

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: allWidths,
    borders: noBorders,
    rows: [new TableRow({ children: cells })],
  });
}

function partnerNoteBox() {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    borders: noBorders,
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: LIGHT_BLUE, type: ShadingType.CLEAR },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 4, color: BLUE },
              bottom: { style: BorderStyle.SINGLE, size: 4, color: BLUE },
              left: { style: BorderStyle.SINGLE, size: 12, color: BLUE },
              right: NO_BORDER,
              insideH: NO_BORDER,
              insideV: NO_BORDER,
            },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Partenariats officiels & approvisionnement garanti",
                    bold: true,
                    size: 20,
                    color: BLUE,
                    font: "Arial",
                  }),
                ],
                spacing: { after: 60 },
              }),
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Eco Air Solutions travaille en partenariat direct avec ces fabricants pour garantir l'approvisionnement en pièces détachées, la garantie constructeur et le support technique.",
                    size: 18,
                    color: DARK_GRAY,
                    font: "Arial",
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
    ],
  });
}

function contactCard() {
  const logoImg = loadImg("logo-square.png", 90, 90);
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1500, 7860],
    borders: noBorders,
    rows: [
      new TableRow({
        children: [
          new TableCell({
            width: { size: 1500, type: WidthType.DXA },
            shading: { fill: BLUE, type: ShadingType.CLEAR },
            margins: { top: 160, bottom: 160, left: 100, right: 100 },
            verticalAlign: VerticalAlign.CENTER,
            children: logoImg
              ? [
                  new Paragraph({
                    children: [logoImg],
                    alignment: AlignmentType.CENTER,
                  }),
                ]
              : [new Paragraph({ children: [] })],
          }),
          new TableCell({
            width: { size: 7860, type: WidthType.DXA },
            shading: { fill: BLUE, type: ShadingType.CLEAR },
            margins: { top: 160, bottom: 160, left: 220, right: 160 },
            verticalAlign: VerticalAlign.CENTER,
            children: [
              new Paragraph({
                children: [
                  new TextRun({
                    text: "Eco Air Solutions",
                    bold: true,
                    size: 28,
                    color: WHITE,
                    font: "Arial",
                  }),
                ],
                spacing: { after: 80 },
              }),
              ...[
                "Demandez votre diagnostic et devis gratuit sous 48h.",
                "Bureau Alger : Cités Vertes, Ouled Fayet, Alger, 16000",
                "Antenne Mila : Rue Boutaf Boulaid, Zeghaia, Mila, 43012",
                "+213 (0) 799 967 458",
                "ecoairsolutions909@gmail.com",
                "https://eco-air-solutions.github.io/",
              ].map(
                (val) =>
                  new Paragraph({
                    children: [
                      new TextRun({
                        text: val,
                        size: 18,
                        color: "CCE8FF",
                        font: "Arial",
                      }),
                    ],
                    spacing: { after: 40 },
                  }),
              ),
            ],
          }),
        ],
      }),
    ],
  });
}

// BRANDS DEFINITIONS (logos filenames as per PDF)
const LOGO_DIR = ""; // same as SRC or separate folder

const climBrands = [
  ["samsung-logo.png", "Samsung"],
  ["lg-logo.png", "LG"],
  ["condor-logo.png", "Condor"],
  ["trane-logo.png", "Trane"],
  ["ciat-logo.png", "CIAT"],
];

const ventilationBrands = [
  ["fa-logo.png", "France Air"],
  ["systemair-logo.png", "Systemair"],
];

const detectionBrands = [
  ["def-logo.png", "DEF"],
  ["abb-logo.png", "ABB"],
];

const desenfBrands = [["dynair-logo.png", "Dynair"]];

const electriciteBrands = [["se-logo.png", "Schneider Electric"]];

// HEADER / FOOTER (unchanged)
function makeHeader() {
  const hi = loadImg("header.png", 660, 88);
  return new Header({
    children: hi
      ? [
          new Paragraph({
            children: [hi],
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 0 },
          }),
        ]
      : [new Paragraph({ children: [] })],
  });
}
function makeFooter() {
  const fi = loadImg("footer.png", 660, 65);
  return new Footer({
    children: [
      fi
        ? new Paragraph({
            children: [fi],
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 0 },
          })
        : new Paragraph({ children: [] }),
      new Paragraph({
        children: [
          new TextRun({ text: "Page ", size: 16, color: MID_GRAY }),
          new TextRun({
            children: [PageNumber.CURRENT],
            size: 16,
            color: MID_GRAY,
          }),
        ],
        alignment: AlignmentType.CENTER,
      }),
    ],
  });
}

const pageProps = {
  page: {
    size: { width: 11906, height: 16838 },
    margin: { top: 720, right: 720, bottom: 720, left: 720 },
  },
};

// DOCUMENT SECTIONS (3 pages exactly like PDF)
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 400, hanging: 240 } } },
          },
        ],
      },
    ],
  },
  sections: [
    // PAGE 1 : cover + intro + stats + domaines
    {
      properties: pageProps,
      headers: { default: makeHeader() },
      footers: { default: makeFooter() },
      children: [
        coverTitleTable(),
        spacer(200),
        logoTaglineTable(),
        spacer(120),
        introPara(),
        spacer(80),
        statsTable(),
        spacer(120),
        sectionHeading("1. NOS DOMAINES D'INTERVENTION"),
        spacer(60),
        sectorIntroPara(),
        spacer(70),
        sectorsGrid(),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    // PAGE 2 : services (A à N) + engagements
    {
      properties: pageProps,
      headers: { default: makeHeader() },
      footers: { default: makeFooter() },
      children: [
        sectionHeading("2. NOS SERVICES"),
        spacer(100),
        ...servicesBlock(),
        spacer(120),
        sectionHeading("3. NOS ENGAGEMENTS"),
        spacer(100),
        engagementsTable(),
        spacer(120),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    // PAGE 3 : marques (toutes catégories) + note + contact
    {
      properties: pageProps,
      headers: { default: makeHeader() },
      footers: { default: makeFooter() },
      children: [
        sectionHeading("4. NOS MARQUES PARTENAIRES"),
        spacer(100),
        brandSectionHeader(
          "CLIMATISATION  —  Systèmes split, VRF & centralisés",
          BLUE,
        ),
        spacer(80),
        brandGrid(climBrands, BLUE),
        spacer(200),
        brandSectionHeader(
          "VENTILATION & AÉRATION  —  CTA, VMC & extraction",
          BLUE,
        ),
        spacer(80),
        brandGrid(ventilationBrands, BLUE),
        spacer(200),
        brandSectionHeader(
          "DÉTECTION INCENDIE  —  SSI, centrales & détecteurs",
          ORANGE,
        ),
        spacer(80),
        brandGrid(detectionBrands, ORANGE),
        spacer(200),
        brandSectionHeader(
          "DÉSENFUMAGE  —  Ventilation & extraction incendie",
          ORANGE,
        ),
        spacer(80),
        brandGrid(desenfBrands, ORANGE),
        spacer(200),
        brandSectionHeader(
          "ÉLECTRICITÉ  —  Matériel électrique, tableaux & armoires",
          BLUE,
        ),
        spacer(80),
        brandGrid(electriciteBrands, BLUE),
        spacer(200),
        partnerNoteBox(),
        spacer(120),
        contactCard(),
      ],
    },
  ],
});

Packer.toBuffer(doc)
  .then((buf) => {
    fs.writeFileSync(OUT, buf);
    console.log("DOCX created:", OUT);
  })
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
