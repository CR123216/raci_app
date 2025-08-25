import streamlit as st
import pandas as pd

st.set_page_config(page_title="Générateur Matrice RACI", layout="wide")
st.title("Générateur de Matrice RACI")
st.write("Répondez aux questions ci-dessous pour générer la matrice RACI pour votre tâche.")

# Les 8 rôles distincts
roles = [
    "Chef de projet",
    "Architecte",
    "Perf système/Quantum Registre",
    "Intégration système",
    "Qualité",
    "Méca",
    "Élec",
    "Optique"
]

# Toutes les questions et assignations (simplification pour ton code)
regles_raci = [
    # 1. Gouvernance et pilotage
    {"question": "La tâche est-elle explicitement mentionnée dans le planning global du projet ?", "assignations": {"Chef de projet": "A"}},
    {"question": "Peut-on avancer sur le prototype si cette tâche n’est pas faite ?", "assignations": {"Chef de projet": "A", "Architecte": "I"}},
    {"question": "Cette tâche doit-elle être validée par une autre équipe avant de continuer ?", "assignations": {"Chef de projet": "A", "Intégration système": "R"}},
    {"question": "Cette tâche doit-elle être validée ou vérifiée par la direction avant de continuer ?", "assignations": {"Chef de projet": "A", "Perf système/Quantum Registre": "R"}},
    {"question": "Si cette tâche n’est pas terminée à temps, le projet prendra-t-il du retard ?", "assignations": {"Chef de projet": "A"}},
    {"question": "La tâche nécessite-t-elle une coordination multi-équipes ?", "assignations": {"Chef de projet": "A", "Architecte": "C", "Intégration système": "C"}},
    {"question": "La tâche engage-t-elle un budget, une ressource critique ou un changement de planning ?", "assignations": {"Chef de projet": "A"}},
    
    # 2. Architecture et design système
    {"question": "La tâche modifie-t-elle la conception globale du système ?", "assignations": {"Architecte": "A", "Intégration système": "C"}},
    {"question": "La tâche impacte-t-elle la roadmap technologique ?", "assignations": {"Architecte": "A", "Intégration système": "C", "Perf système/Quantum Registre": "C"}},
    {"question": "La tâche nécessite-t-elle de définir de nouvelles spécifications système ?", "assignations": {"Architecte": "R", "Chef de projet": "I", "Intégration système": "C"}},
    
    # 3. Intégration système
    {"question": "La tâche consiste-t-elle à assembler ou mettre en place un sous-système ?", "assignations": {"Intégration système": "R"}},
    {"question": "Vérification de l’intégration des modules métiers ?", "assignations": {"Intégration système": "R", "Qualité": "C"}},
    {"question": "La tâche implique-t-elle une manipulation connue <30min ?", "assignations": {"Intégration système": "I"}},
    {"question": "Préparer un environnement de test système ?", "assignations": {"Intégration système": "R", "Perf système/Quantum Registre": "C"}},
    
    # 4. Performance système
    {"question": "Mesurer ou caractériser la performance du système ?", "assignations": {"Perf système/Quantum Registre": "R"}},
    {"question": "Définir les métriques de performance ?", "assignations": {"Perf système/Quantum Registre": "A", "Architecte": "C"}},
    {"question": "Identifier et analyser les goulets d’étranglement ?", "assignations": {"Perf système/Quantum Registre": "R", "Chef de projet": "I"}},
    
    # 5. Métiers techniques
    {"question": "Conception ou modification mécanique ?", "assignations": {"Méca": "R", "Architecte": "C", "Intégration système": "I"}},
    {"question": "Conception ou correction électronique ?", "assignations": {"Élec": "R", "Intégration système": "I", "Qualité": "C"}},
    {"question": "Alignement ou calibration optique ?", "assignations": {"Optique": "R", "Perf système/Quantum Registre": "C", "Intégration système": "I"}},
    {"question": "Exigence normative ou traçabilité ?", "assignations": {"Qualité": "A"}},
    
    # 6. Quantum Registre
    {"question": "Définir de nouveaux patterns de piégeage ?", "assignations": {"Perf système/Quantum Registre": "R", "Architecte": "I"}},
    {"question": "Exécuter des séquences de test atomiques ?", "assignations": {"Perf système/Quantum Registre": "R", "Perf système/Quantum Registre": "C"}},
    {"question": "Vérifier les patterns respectent les contraintes ?", "assignations": {"Perf système/Quantum Registre": "C", "Architecte": "A"}},
    
    # 7. Contraintes et exceptions
    {"question": "Résolution rapide d’un problème connu <30min ?", "assignations": {"Intégration système": "I"}},
    {"question": "Tâche exploratoire (R&D) ?", "assignations": {"Architecte": "A", "Perf système/Quantum Registre": "C"}},
    {"question": "Impacte la disponibilité du banc ou cryostat ?", "assignations": {"Intégration système": "A", "Chef de projet": "I"}}
]

# Stockage des réponses
matrice_data = []

for idx, q in enumerate(regles_raci):
    reponse = st.radio(q["question"], ("Oui", "Non"), key=f"q{idx}")
    ligne = {role: "" for role in roles}  # initialise toutes les colonnes vides
    if reponse == "Oui":
        for role, action in q["assignations"].items():
            if role in roles:
                ligne[role] = action
    ligne["Question"] = q["question"]
    matrice_data.append(ligne)

# Création DataFrame
df_raci = pd.DataFrame(matrice_data)
df_raci = df_raci[["Question"] + roles]

# Affichage
if st.button("Afficher la matrice RACI"):
    st.subheader("Matrice RACI compacte")
    st.dataframe(df_raci)

