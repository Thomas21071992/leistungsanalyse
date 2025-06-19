import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏃 Leistungsdiagnostik Tool", layout="wide")
st.title("🏃 Leistungsdiagnostik Tool mit Fortschritts- und Vergleichsanalyse")

# Eingabemaske
name = st.text_input("Name", value="")
alter = st.number_input("Alter", value=30, min_value=6, max_value=99)
geschlecht = st.selectbox("Geschlecht", ["männlich", "weiblich"])
sprint = st.number_input("30m Sprintzeit Handstoppung (in Sekunden)", value=4.5)
sprung = st.number_input("Sprunghöhe (in cm)", value=50)
liegestuetzen = st.number_input("Liegestütze am Stück", value=15)

# Simulierte Vergleichsdaten (vereinfacht)
def durchschnittswerte(alter, geschlecht):
    if geschlecht == "männlich":
        return {
            "sprint": 4.5 - 0.02 * max(0, 35 - alter),
            "sprung": 45 + 0.5 * max(0, 35 - alter),
            "liegestuetzen": 12 + 0.3 * max(0, 35 - alter),
        }
    else:
        return {
            "sprint": 4.7 - 0.015 * max(0, 35 - alter),
            "sprung": 35 + 0.4 * max(0, 35 - alter),
            "liegestuetzen": 8 + 0.25 * max(0, 35 - alter),
        }

# CSV-Verwaltung
log_file = "leistungs_log.csv"
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["Name", "Datum", "Alter", "Geschlecht", "Sprintzeit", "Sprunghöhe", "Liegestütze", "Bewertung"])

# Bewertung vorbereiten (ohne Button)
bewertung = "Gut"
if sprint < 4.2 and sprung > 60 and liegestuetzen > 25:
    bewertung = "Sehr gut"
elif sprint > 4.6 or sprung < 40 or liegestuetzen < 10:
    bewertung = "Ausbaufähig"

# Auswahl der Einheiten je Disziplin vor dem Button (wenn ausbaufähig)
einheiten_sprint = 1
einheiten_sprung = 1
einheiten_liegestuetzen = 1

if bewertung == "Ausbaufähig":
    if sprint > 4.6:
        einheiten_sprint = st.selectbox("Sprint - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)
    if sprung < 40:
        einheiten_sprung = st.selectbox("Sprungkraft - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)
    if liegestuetzen < 10:
        einheiten_liegestuetzen = st.selectbox("Liegestütze - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)

if st.button("Analyse starten"):
    if not name:
        st.error("❗ Bitte gib deinen Namen ein.")
    else:
        # Trainingsvorschläge erzeugen
        trainingsvorschläge = []

        if sprint > 4.6:
            if einheiten_sprint == 1:
                trainingsvorschläge.append("""
                ### 🏃 Sprinttraining (1 Einheit/Woche)
                - 5x 30m Sprints mit maximaler Intensität
                - 3 Minuten Pause zwischen den Sprints
                - Fokus auf explosiven Start und Technik
                """)
            else:
                trainingsvorschläge.append("""
                ### 🏃 Sprinttraining (2 Einheiten/Woche)
                **Einheit 1:**
                - 5x 30m Sprints maximal
                - 3 Minuten Pause
                - Technikfokus Start
                                           
                **Einheit 2:**
                - 4x 60m Sprints im aeroben Bereich
                - 5 Minuten Pause
                - Laufökonomie und Entspannung
                """)

        if sprung < 40:
            if einheiten_sprung == 1:
                trainingsvorschläge.append("""
                ### 🦵 Sprungkraft (1 Einheit/Woche)
                - 3x10 Box Jumps
                - 3x8 Tiefsprünge mit sofortigem Hochsprung
                - 2x12 Bulgarian Split Squats
                """)
            else:
                trainingsvorschläge.append("""
                ### 🦵 Sprungkraft (2 Einheiten/Woche)
                **Einheit 1:**
                - 3x10 Box Jumps
                - 3x8 Tiefsprünge mit Hochsprung
                - Core-Stabilität: 3x 30 Sek. Planks
                                           
                **Einheit 2:**
                - 3x12 Bulgarian Split Squats
                - 3x10 einbeinige Kniebeugen
                - Sprungkoordinationstraining (Seilspringen)
                """)

        if liegestuetzen < 10:
            if einheiten_liegestuetzen == 1:
                trainingsvorschläge.append("""
                ### 💪 Liegestütze (1 Einheit/Woche)
                - 3–5 Sätze Liegestütze bis fast Muskelversagen
                - 3x8 Negativ-Liegestütze (4 Sek. Absenken)
                - Core & Schulter: 3x 60 Sek. Plank
                """)
            else:
                trainingsvorschläge.append("""
                ### 💪 Liegestütze (2 Einheiten/Woche)
                **Einheit 1:**
                - 3x 5–8 Sätze Liegestütze bis Muskelversagen
                - 3x8 Negativ-Liegestütze
                - Schulterstabilisation: 3x 15 Sek. Schulter-Taps
                                           
                **Einheit 2:**
                - 3x 12 Liegestütze mit Pausen
                - 3x60 Sek. Planks
                - Dynamische Core-Übungen (Russian Twists)
                """)

        # Bewertung speichern (wie vorher)
        if sprint < 4.2 and sprung > 60 and liegestuetzen > 25:
            bewertung = "Sehr gut"
        elif sprint > 4.6 or sprung < 40 or liegestuetzen < 10:
            bewertung = "Ausbaufähig"
        else:
            bewertung = "Gut"

        new_entry = {
            "Name": name,
            "Datum": datetime.now().strftime("%Y-%m-%d"),
            "Alter": alter,
            "Geschlecht": geschlecht,
            "Sprintzeit": sprint,
            "Sprunghöhe": sprung,
            "Liegestütze": liegestuetzen,
            "Bewertung": bewertung
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(log_file, index=False)
        st.success(f"{name}, deine Bewertung: **{bewertung}** wurde gespeichert ✅")

        # Ausgabe der Trainingsvorschläge
        if trainingsvorschläge:
            st.markdown("## 💡 Trainingsvorschläge zur Leistungssteigerung:")
            for vorschlag in trainingsvorschläge:
                st.markdown(vorschlag)
        else:
            st.markdown("✅ Deine Leistungen sind sehr gut – weiter so!")

        # Vergleichsdaten
        d = durchschnittswerte(alter, geschlecht)

        # Visualisierung je Disziplin
        st.markdown("## 📊 Vergleich mit Durchschnitt deiner Altersklasse")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**30m Sprintzeit**")
            fig, ax = plt.subplots()
            ax.bar(["Du", "Ø"], [sprint, d["sprint"]], color=["skyblue", "gray"])
            ax.set_ylabel("Sekunden")
            st.pyplot(fig)

        with col2:
            st.markdown("**Sprunghöhe**")
            fig, ax = plt.subplots()
            ax.bar(["Du", "Ø"], [sprung, d["sprung"]], color=["orange", "gray"])
            ax.set_ylabel("cm")
            st.pyplot(fig)

        with col3:
            st.markdown("**Liegestütze**")
            fig, ax = plt.subplots()
            ax.bar(["Du", "Ø"], [liegestuetzen, d["liegestuetzen"]], color=["green", "gray"])
            ax.set_ylabel("Wiederholungen")
            st.pyplot(fig)

        # Verlauf anzeigen
        st.markdown("## 🧾 Verlauf deiner Leistungen")
        user_df = df[df["Name"] == name].copy()
        st.dataframe(user_df.tail(5))

        if len(user_df) > 1:
            st.line_chart(user_df.set_index("Datum")[["Sprintzeit", "Sprunghöhe", "Liegestütze"]])
