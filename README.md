# 📊 Analyse des Données Éducatives avec Power BI

Projet de Data Analytics réalisé dans le cadre du bootcamp **Data Analyst — CCFBS / [INT-Maroc] DATA Analyst**.

L'objectif est d'exploiter un jeu de données d'exemple décrivant un établissement scolaire fictif (élèves, enseignants, cours) afin de **nettoyer, modéliser, transformer et visualiser** les données dans un tableau de bord Power BI complet et interactif, destiné à appuyer les décisions stratégiques de la direction.

---

## 🗂️ Structure du repo

```
.
├── data/
│   ├── students.csv      # Informations sur les élèves
│   ├── teachers.csv      # Informations sur les enseignants
│   └── courses.csv       # Détail des cours et résultats
├── powerbi/
│   └── dashboard.pbix    # Fichier Power BI (modèle + rapport)
├── .gitignore
└── README.md
```

---

## 📁 Jeux de données

| Fichier | Description | Colonnes clés |
|---|---|---|
| `students.csv` | 120 élèves | `student_id`, `class_level`, `section`, `status`, `average_grade`, `absences_count`, `teacher_id` |
| `teachers.csv` | 20 enseignants | `teacher_id`, `subject`, `contract_type`, `weekly_hours`, `performance_rating` |
| `courses.csv` | 500 cours | `course_id`, `teacher_id`, `student_id`, `semester`, `year`, `grade`, `pass_fail` |

---

## 🧹 Étapes du projet

### 1. Exploration & Profilage
Profilage des colonnes dans Power Query : valeurs manquantes, doublons, incohérences de format (ex. `gender`: `M/F/female/Femme`), valeurs aberrantes.

### 2. Nettoyage (Power Query)
- Imputation par médiane (notes, absences) / valeur `Inconnu` (texte)
- Standardisation des formats (dates, casse, espaces)
- Colonnes calculées :
  - `age_eleve`
  - `anciennete_enseignant`
  - `taux_realisation` (`completed_hours / scheduled_hours × 100`)
  - `annee_inscription`

### 3. Modélisation
- Relations : `students[teacher_id] → teachers`, `courses[student_id] → students`, `courses[teacher_id] → teachers`
- Table calendrier `DimDate` (DAX `CALENDAR`) reliée à `students[enrollment_date]`

### 4. Mesures DAX (`_Mesures`)
`Total Élèves` · `Moyenne Générale` · `Taux de Réussite` · `Élèves à Risque` · `Heures Moy. par Enseignant` · `Top Matières` · `Évolution Inscriptions`

### 5. Visualisations (3 pages)
| Page | Contenu |
|---|---|
| **Vue Élèves** | KPIs, répartition par niveau/section, évolution des inscriptions, corrélation absences/moyenne, répartition par statut |
| **Vue Enseignants** | KPIs, répartition matière/contrat, distribution des évaluations, Top 5 / Flop 5 enseignants |
| **Vue Cours & Résultats** | KPIs, réussite/échec par matière, évolution des notes, matières avec moyenne ≥ 12 |

### 6. Interactivité
Slicers (année, niveau, matière, type de contrat, semestre), interactions entre visuels, bouton de réinitialisation des filtres.

### 7. Insights & Recommandations
Synthèse des matières à fort taux d'échec, charge de travail des enseignants, profil des élèves à risque — page **Conclusions** dédiée dans le rapport.

---

## 🛠️ Outils utilisés
- **Power BI Desktop** (Power Query, DAX, modélisation, visualisations)
- **DAX** pour les mesures et colonnes calculées
- **Jira** pour le suivi du projet

## 👤 Auteur
Brahim — Data Analyst / Data Engineer junior, bootcamp CCFBS (depuis janvier 2025)

## 📅 Deadline
Assigné le 22/06/2026 — Deadline le 26/06/2026

## Qualité des données sources

Les trois fichiers CSV contiennent 120 élèves uniques, 20 enseignants et 500 lignes de cours. Quatre lignes strictement identiques ont été retirées de `students.csv` après contrôle des identifiants, sans supprimer d'élèves distincts.
Les clés, les références croisées et les bornes des heures planifiées/réalisées sont vérifiées par `tests/test_source_data.py`.
Certaines notes et certains résultats de cours sont absents : **32 cours sur 500**. De plus, **22 cours sur 500** n'ont pas de valeur `completed_hours`. Le taux de réalisation doit ignorer ces valeurs manquantes plutôt que les interpréter comme zéro.
Ces lignes ne doivent pas être automatiquement comptées comme des échecs lors du calcul du taux de réussite. Le dénominateur d'un taux de réussite fondé sur `pass_fail` doit être limité aux cours dont le résultat est connu.

Pour contrôler les fichiers sources :

```bash
python -m unittest discover -s tests -v
```

Ce contrôle porte sur les CSV, pas sur la justesse d'exécution du fichier Power BI `.pbix`, qui reste à vérifier dans Power BI Desktop.
