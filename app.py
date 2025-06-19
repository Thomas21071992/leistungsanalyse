import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="🏃 Leistungsdiagnostik Tool", layout="wide")
st.title("🏃 Leistungsdiagnostik Tool (50 m Sprint, Standweitsprung, Liegestütze)")

# Eingabemaske
name = st.text_input("Name", value="")
alter = st.number_input("Alter", value=30, min_value=6, max_value=99)
geschlecht = st.selectbox("Geschlecht", ["männlich", "weiblich"])
sprint = st.number_input("50 m Sprintzeit (in Sekunden)", value=8.0)
sprung = st.number_input("Standweitsprung (in cm)", value=180)
liegestuetzen = st.number_input("Liegestütze am Stück", value=15)

# Vergleichswerte
def durchschnittswerte(alter, geschlecht):
    if geschlecht == "männlich":
        return {
            "sprint": 7.8 - 0.02 * max(0, 35 - alter),
            "sprung": 180 + 1.0 * max(0, 35 - alter),
            "liegestuetzen": 12 + 0.3 * max(0, 35 - alter),
        }
    else:
        return {
            "sprint": 8.2 - 0.015 * max(0, 35 - alter),
            "sprung": 150 + 0.8 * max(0, 35 - alter),
            "liegestuetzen": 8 + 0.25 * max(0, 35 - alter),
        }

# Bewertung
bewertung = "Gut"
if sprint < 7.5 and sprung > 200 and liegestuetzen > 25:
    bewertung = "Sehr gut"
elif sprint > 8.5 or sprung < 160 or liegestuetzen < 10:
    bewertung = "Ausbaufähig"

# Einheitenauswahl
einheiten_sprint = 1
einheiten_sprung = 1
einheiten_liegestuetzen = 1

if bewertung == "Ausbaufähig":
    if sprint > 8.5:
        einheiten_sprint = st.selectbox("Sprint - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)
    if sprung < 160:
        einheiten_sprung = st.selectbox("Sprungkraft - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)
    if liegestuetzen < 10:
        einheiten_liegestuetzen = st.selectbox("Liegestütze - Anzahl Trainingseinheiten pro Woche", [1, 2], index=0)

# CSV-Verwaltung
log_file = "leistungs_log.csv"
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["Name", "Datum", "Alter", "Geschlecht", "Sprintzeit", "Sprungweite", "Liegestütze", "Bewertung"])

if st.button("Analyse starten"):
    if not name:
        st.error("❗ Bitte gib deinen Namen ein.")
    else:
        # Speichern
        new_entry = {
            "Name": name,
            "Datum": datetime.now().strftime("%Y-%m-%d"),
            "Alter": alter,
            "Geschlecht": geschlecht,
            "Sprintzeit": sprint,
            "Sprungweite": sprung,
            "Liegestütze": liegestuetzen,
            "Bewertung": bewertung
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(log_file, index=False)
        st.success(f"{name}, deine Bewertung: **{bewertung}** wurde gespeichert ✅")

        # Trainingsvorschläge
        trainingsvorschläge = []

        if bewertung == "Sehr gut":
            st.markdown("## 🏋️ Allgemeiner Trainingsplan (2x pro Woche)")
            st.markdown("""
            ### 🏃 Sprint & Lauftechnik
            - 4x 50 m Sprint mit 95% Intensität  
            - 3x 30 m Technikstarts  
            - 2x 80 m lockeres Sprinten

            ### 🦵 Sprungkraft & Beine
            - 3x10 Box Jumps  
            - 3x10 einbeinige Squats  
            - 3x20 Seilsprünge

            ### 💪 Oberkörper & Core
            - 3x max. Liegestütze  
            - 3x8 Negativ-Liegestütze  
            - 3x 60 Sek. Planks (vorn + Seite)

            ➕ Bonus: 10 Min. Mobility & Stretching
            """)
        elif bewertung == "Ausbaufähig":
            if sprint > 8.5:
                if einheiten_sprint == 1:
                    trainingsvorschläge.append("""
                    ### 🏃 Sprinttraining (1x/Woche)
                    - 5x 50m Sprint mit 90–95% Intensität  
                    - 3 Min Pause  
                    - Startübungen: Kniehub, Anfersen
                    """)
                else:
                    trainingsvorschläge.append("""
                    ### 🏃 Sprinttraining (2x/Woche)
                    **Einheit 1:**  
                    - 5x 50m Sprint maximal  
                    - 4 Min Pause  
                    - Technikstarts aus 3-Punkt-Position
                    
                    **Einheit 2:**  
                    - 3x 80m Sprint locker  
                    - 3x 30m Techniklauf (Videofeedback)
                    """)

            if sprung < 160:
                if einheiten_sprung == 1:
                    trainingsvorschläge.append("""
                    ### 🦵 Standweitsprung (1x/Woche)
                    - 4x5 Standweitsprünge  
                    - 3x10 Box Jumps  
                    - 3x15 Seilspringen
                    """)
                else:
                    trainingsvorschläge.append("""
                    ### 🦵 Standweitsprung (2x/Woche)
                    **Einheit 1:**  
                    - 4x5 Standweitsprünge  
                    - 3x8 Tiefsprünge  
                    - Core: 3x30 Sek. Plank
                    
                    **Einheit 2:**  
                    - 3x12 Bulgarian Split Squats  
                    - 3x Skater-Jumps  
                    - 3x Seilspringen (Koordination)
                    """)

            if liegestuetzen < 10:
                if einheiten_liegestuetzen == 1:
                    trainingsvorschläge.append("""
                    ### 💪 Liegestütze (1x/Woche)
                    - 4 Sätze bis Erschöpfung  
                    - 3x10 Negativ-Liegestütze  
                    - 3x45 Sek. Plank
                    """)
                else:
                    trainingsvorschläge.append("""
                    ### 💪 Liegestütze (2x/Woche)
                    **Einheit 1:**  
                    - 5x max. Liegestütze  
                    - 3x8 Negativ-Liegestütze  
                    - Schulterstabi: 3x15 Sek. Taps
                    
                    **Einheit 2:**  
                    - 3x12 Liegestütze mit Pausen  
                    - 3x60 Sek. Plank  
                    - Core: Russian Twists
                    """)

            st.markdown("## 💡 Trainingsvorschläge zur Verbesserung:")
            for block in trainingsvorschläge:
                st.markdown(block)
        else:
            st.info("Deine Leistung ist solide – du kannst bei Bedarf gezielt trainieren oder deinen Zustand erhalten.")

        # Vergleichsdaten
        d = durchschnittswerte(alter, geschlecht)

        st.markdown("## 📊 Vergleich mit Durchschnitt deiner Altersgruppe")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**50 m Sprintzeit**")
            fig, ax = plt.subplots()
            ax.bar(["Du", "Ø"], [sprint, d["sprint"]], color=["skyblue", "gray"])
            ax.set_ylabel("Sekunden")
            st.pyplot(fig)

        with col2:
            st.markdown("**Standweitsprung**")
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

        # Verlauf
        st.markdown("## 📈 Verlauf deiner Einträge")
        user_df = df[df["Name"] == name].copy()
        st.dataframe(user_df.tail(5))

        if len(user_df) > 1:
            st.line_chart(user_df.set_index("Datum")[["Sprintzeit", "Sprungweite", "Liegestütze"]])

# 🔐 Adminbereich
st.markdown("---")
st.markdown("## 🔐 Adminbereich")

admin_passwort = st.text_input("Admin-Passwort eingeben:", type="password")

if admin_passwort == "sportadmin2025":
    st.success("✅ Adminzugriff gewährt.")
    
    if st.button("📥 CSV herunterladen"):
        st.download_button(
            label="📄 Gesamte Leistungsdaten herunterladen",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="leistungs_log.csv",
            mime="text/csv"
        )
else:
    if admin_passwort:
        st.error("❌ Falsches Passwort.")

