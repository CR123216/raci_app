import streamlit as st
import pandas as pd

st.set_page_config(page_title="Arbre de décision RACI", layout="centered")
st.title("🌳 Arbre de décision RACI")

# ----------------------------
# Étape 1 – Type de projet
# ----------------------------
st.header("Étape 1 – Type de projet")
type_projet = None

if st.radio("Est-ce un projet Lab (investiguer un concept en setup de labo) ?", ["Oui", "Non"]) == "Oui":
    type_projet = "Lab"
    tech_lead = "Quantum"
elif st.radio("Est-ce un projet POC (développer une nouvelle fonctionnalité testée sur QPU R&D) ?", ["Oui", "Non"]) == "Oui":
    type_projet = "POC"
    tech_lead = "Performance"
elif st.radio("Est-ce un projet PROTO (fonctionnalité implémentée sur un produit) ?", ["Oui", "Non"]) == "Oui":
    type_projet = "PROTO"
    tech_lead = "Intégration"
else:
    st.warning("⚠️ Clarification nécessaire avec le chef de projet.")

# Stockage des assignations RACI
assignations = []

if type_projet:
    st.success(f"Projet identifié : **{type_projet}** | Tech Lead = {tech_lead}")

    # ----------------------------
    # Étape 2 – Nature de la tâche
    # ----------------------------
    st.header("Étape 2 – Nature de la tâche")

    # Bloc A – Définition amont
    st.subheader("Bloc A – Définition amont")
    if st.checkbox("La tâche consiste-t-elle à participer à la définition des besoins amonts ?"):
        assignations.append((tech_lead, "A"))
        assignations.append(("Chef de projet", "A"))
        assignations.append(("Métiers", "C"))

    if st.checkbox("La tâche implique-t-elle de prendre en compte les contraintes d’intégration ?"):
        if type_projet == "PROTO":
            assignations.append(("Intégration", "R"))
        elif type_projet == "POC":
            assignations.append(("Performance", "A"))
        elif type_projet == "Lab":
            assignations.append(("Quantum", "A"))

    if st.checkbox("La tâche consiste-t-elle en la définition du système ou la synthèse de l’ICD ?"):
        assignations.append((tech_lead, "R/A"))

    # Bloc B – Design et stratégie de test
    st.subheader("Bloc B – Design et stratégie de test")
    if st.checkbox("La tâche consiste-t-elle à définir ou valider les éléments de design nécessaires à l’intégration ?"):
        assignations.append((tech_lead, "R"))
        assignations.append(("Métiers", "C"))

    if st.checkbox("La tâche consiste-t-elle à définir la stratégie de test ?"):
        assignations.append((tech_lead, "A"))
        assignations.append(("Métiers", "R"))
        assignations.append(("Autres équipes", "C"))

    # Bloc C – Intégration et validation
    st.subheader("Bloc C – Intégration et validation")
    if st.checkbox("La tâche consiste-t-elle à intégrer le QPU (HW ou SW) ?"):
        if type_projet == "PROTO":
            assignations.append(("Intégration", "R"))
        elif type_projet == "POC":
            assignations.append(("Performance", "A"))
        elif type_projet == "Lab":
            assignations.append(("Quantum", "A"))

    if st.checkbox("La tâche consiste-t-elle à appliquer les tests d’intégration et vérifier leur couverture ?"):
        assignations.append((tech_lead, "R"))
        assignations.append(("Autres équipes", "C"))

    # Bloc D – Optimisation et passation
    st.subheader("Bloc D – Optimisation et passation")
    if st.checkbox("Après les tests systèmes, la tâche concerne-t-elle l’optimisation du système ?"):
        assignations.append(("Performance", "A"))

    if st.checkbox("La tâche consiste-t-elle à assurer la passation vers Méthodes/Production ?"):
        if type_projet == "PROTO":
            assignations.append(("Intégration", "R"))
        elif type_projet == "POC":
            assignations.append(("Performance", "C"))
        elif type_projet == "Lab":
            assignations.append(("Quantum", "C"))

    # ----------------------------
    # Résultat : Matrice RACI
    # ----------------------------
    if assignations:
        st.header("📊 Matrice RACI générée")
        df = pd.DataFrame(assignations, columns=["Rôle", "Action"])
        df = df.groupby("Rôle")["Action"].apply(lambda x: "/".join(sorted(set(x)))).reset_index()
        st.dataframe(df)
    else:
        st.info("👉 Sélectionne des réponses pour générer la matrice RACI.")

