import streamlit as st
import pandas as pd

st.set_page_config(page_title="Générateur Matrice RACI", layout="wide")

st.title("Générateur de Matrice RACI")
st.write("Répondez aux questions ci-dessous pour générer la matrice RACI pour votre tâche.")

# Définition des règles RACI
regles_raci = {
    "1. Gouvernance et pilotage": [
        {"question": "La tâche est-elle explicitement mentionnée dans le planning global du projet ?", "assignations": {"Chef de projet": "A"}},
        {"question": "La tâche est-elle une condition de passage pour un prototype ?", "assignations": {"Chef de projet": "A", "Architecte": "I"}},
        {"question": "La tâche est-elle associée à une livraison interne validée par la direction technique ?", "assignations": {"Chef de projet": "A", "Métier exécutant": "R"}},
        {"question": "La tâche est-elle un milestone formel suivi par le steering committee ou les sponsors ?", "assignations": {"Chef de projet": "A", "Perf système/Quantum Registre": "R"}},
        {"question": "Si la tâche échoue ou est retardée, cela a-t-il un impact direct sur le calendrier officiel ?", "assignations": {"Chef de projet": "A"}},
        {"question": "La tâche nécessite-t-elle une coordination multi-équipes ?", "assignations": {"Chef de projet": "A", "Architecte": "C", "Intégration système": "C"}},
        {"question": "La tâche engage-t-elle un budget, une ressource critique ou un changement de planning ?", "assignations": {"Chef de projet": "A", "Métiers impactés": "C"}},
    ],
    "2. Architecture et design système": [
        {"question": "La tâche modifie-t-elle la conception globale du système ?", "assignations": {"Architecte": "A", "Intégration système": "C", "Métiers concernés": "C"}},
        {"question": "La tâche impacte-t-elle la roadmap technologique ?", "assignations": {"Architecte": "A", "Intégration système": "C (si contraintes physiques)", "Perf système": "C", "Chef de projet": "I"}},
        {"question": "La tâche nécessite-t-elle de définir de nouvelles spécifications système ?", "assignations": {"Architecte": "R", "Chef de projet": "I", "Intégration système": "C", "Métiers": "C"}},
    ],
    "3. Intégration système": [
        {"question": "La tâche consiste-t-elle à assembler ou mettre en place physiquement un sous-système ?", "assignations": {"Intégration système": "R"}},
        {"question": "La tâche vise-t-elle à vérifier l'intégration des modules métiers ?", "assignations": {"Intégration système": "R", "Qualité": "C", "Métiers": "I"}},
        {"question": "La tâche implique-t-elle de reproduire une manipulation connue (<30 min) ?", "assignations": {"Métier concerné": "R", "Intégration": "I"}},
        {"question": "La tâche consiste-t-elle à préparer un environnement de test système ?", "assignations": {"Intégration système": "R", "Perf système": "C", "Métier": "C/I"}},
    ],
    "4. Performance système": [
        {"question": "La tâche consiste-t-elle à mesurer ou caractériser la performance du système ?", "assignations": {"Perf système": "R", "Métiers concernés": "C"}},
        {"question": "La tâche définit-elle les métriques de performance ou seuils attendus ?", "assignations": {"Perf système": "A", "Architecte": "C"}},
        {"question": "La tâche demande-t-elle d’analyser les goulets d’étranglement ?", "assignations": {"Perf système": "R", "Métiers": "C", "Chef de projet": "I"}},
    ],
    "5. Métiers techniques": [
        {"question": "La tâche concerne-t-elle la conception mécanique ?", "assignations": {"Méca": "R", "Architecte": "C", "Intégration": "I"}},
        {"question": "La tâche implique-t-elle un schéma électronique ?", "assignations": {"Élec": "R", "Intégration": "I", "Qualité": "C"}},
        {"question": "La tâche demande-t-elle un alignement optique ?", "assignations": {"Optique": "R", "Perf système": "C", "Intégration": "I"}},
        {"question": "La tâche comporte-t-elle une exigence normative ou de traçabilité ?", "assignations": {"Qualité": "A", "Équipe exécutante": "R"}},
    ],
    "6. Quantum Registre": [
        {"question": "La tâche consiste-t-elle à définir de nouveaux patterns de piégeage ?", "assignations": {"Quantum Registre": "R", "Architecte": "I"}},
        {"question": "La tâche demande-t-elle d’exécuter des séquences de test atomique ?", "assignations": {"Quantum Registre": "R", "Perf système": "C"}},
        {"question": "La tâche implique-t-elle de vérifier les patterns par rapport au système ?", "assignations": {"Quantum Registre": "C", "Architecte": "A"}},
    ],
    "7. Contraintes et exceptions": [
        {"question": "La tâche est-elle une résolution rapide d’un problème connu (<30 min) ?", "assignations": {"Métier concerné": "R", "Intégration": "I", "Chef de projet": "non impliqué"}},
        {"question": "La tâche est-elle exploratoire ?", "assignations": {"Métiers concernés": "R", "Architecte": "A", "Perf système": "C"}},
        {"question": "La tâche impacte-t-elle la disponibilité du banc ou cryostat ?", "assignations": {"Intégration": "A", "Métiers concernés": "R", "Chef de projet": "I"}},
    ]
}

# Stockage des réponses
raci_final = {}

# Parcours des catégories et questions
for categorie, questions in regles_raci.items():
    st.header(categorie)
    for q in questions:
        reponse = st.radio(q["question"], ("Oui", "Non"), key=f"{categorie}_{q['question']}")
        if reponse == "Oui":
            for role, action in q["assignations"].items():
                raci_final[role] = action

# Affichage de la matrice RACI
if st.button("Afficher la matrice RACI"):
    st.subheader("Matrice RACI générée")
    if raci_final:
        df = pd.DataFrame(list(raci_final.items()), columns=["Rôle", "Action"])
        st.table(df)
    else:
        st.write("Aucune assignation RACI sélectionnée.")
