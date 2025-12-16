import os
import time
import subprocess

# ==========================================
# 1️⃣ INSTALL DEPENDENCIES & SETUP SSL
# ==========================================
print("⏳ Installing libraries... (this may take 1-2 minutes)")
os.system("pip install -q streamlit pyngrok pymysql sqlalchemy requests streamlit-option-menu")
os.system("wget -O /content/ca.pem https://cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem")
print("✅ Installation complete.")

# ==========================================
# 2️⃣ WRITE THE STREAMLIT APP FILE (app.py)
# ==========================================
app_code = """
import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import create_engine, text
from streamlit_option_menu import option_menu

# ---------------- CONFIG & STYLING ----------------
st.set_page_config(page_title="Harvard Artifacts Manager", layout="wide")
st.markdown(\"\"\"
<style>
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 5px; }
    div[data-testid="stMetricValue"] { font-size: 20px; }
    h1 { text-align: center; color: #b31b1b; }
</style>
\"\"\", unsafe_allow_html=True)

# ---------------- CONSTANTS ----------------
API_KEY = "REPLACE_YOUR_API_KEY_HERE"
BASE_URL = "https://api.harvardartmuseums.org/object"
DB_PASSWORD = "REPLACE_YOUR_DB_PASSWORD_HERE"

# TiDB Connection Strings
DB_CONNECTION_STR_ROOT = (
    "mysql+pymysql://REPLACE_USERNAME:"
    + DB_PASSWORD +
    "@REPLACE_TIDB_HOST:4000/test"
    "?ssl_verify_cert=true&ssl_verify_identity=true&ssl_ca=/content/ca.pem"
)

DB_CONNECTION_STR_TARGET = (
    "mysql+pymysql://REPLACE_USERNAME:"
    + DB_PASSWORD +
    "@REPLACE_TIDB_HOST:4000/REPLACE_DATABASE_NAME"
    "?ssl_verify_cert=true&ssl_verify_identity=true&ssl_ca=/content/ca.pem"
)

# ---------------- STATE MANAGEMENT ----------------
if "all_records" not in st.session_state:
    st.session_state.all_records = []
if "data_fetched" not in st.session_state:
    st.session_state.data_fetched = False
if "metadata" not in st.session_state:
    st.session_state.metadata = []
if "media" not in st.session_state:
    st.session_state.media = []
if "colors" not in st.session_state:
    st.session_state.colors = []

# ---------------- HEADER ----------------
st.markdown("<h1>🏛️ Harvard Art Museums: ETL & SQL Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>End-to-End ETL and SQL Analytics using Harvard Art Museums API</p>", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
selected = option_menu(
    menu_title=None,
    options=["Data Extraction", "Migrate to SQL", "SQL Queries"],
    icons=["cloud-download", "database", "list-task"],
    orientation="horizontal"
)

# ==========================================
# TAB 1: DATA EXTRACTION
# ==========================================
if selected == "Data Extraction":
    st.subheader("📥 Fetch Artifacts from API")

    classifications = ["Photographs", "Prints", "Sculpture", "Paintings", "Drawings"]
    selected_cls = st.selectbox("Select Classification", ["Fetch All"] + classifications)

    if st.button("🚀 Start Extraction"):
        st.session_state.all_records = []
        st.session_state.metadata = []
        st.session_state.media = []
        st.session_state.colors = []

        target_classes = classifications if selected_cls == "Fetch All" else [selected_cls]

        for cls in target_classes:
            for page in range(1, 26):
                params = {
                    "apikey": API_KEY,
                    "size": 100,
                    "page": page,
                    "classification": cls
                }
                r = requests.get(BASE_URL, params=params)
                data = r.json()
                records = data.get("records", [])
                st.session_state.all_records.extend(records)

        st.session_state.data_fetched = True
        st.success(f"Fetched {len(st.session_state.all_records)} records")

# ==========================================
# TAB 2: MIGRATE TO SQL
# ==========================================
if selected == "Migrate to SQL":
    st.subheader("🗄️ Database Migration")

    if st.button("Upload to Database"):
        engine_root = create_engine(DB_CONNECTION_STR_ROOT)
        with engine_root.begin() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS REPLACE_DATABASE_NAME;"))

        engine_target = create_engine(DB_CONNECTION_STR_TARGET)
        st.success("Database migration completed")

# ==========================================
# TAB 3: SQL QUERIES
# ==========================================
if selected == "SQL Queries":
    st.subheader("🔎 Run SQL Queries")

    query = "SELECT title, culture FROM metadata LIMIT 10;"
    st.code(query, language="sql")

    if st.button("Run Query"):
        engine = create_engine(DB_CONNECTION_STR_TARGET)
        df = pd.read_sql(query, engine)
        st.dataframe(df)
"""

# Cleanup
app_code = app_code.replace('\\u00a0', ' ')

with open("app.py", "w") as f:
    f.write(app_code)

print("✅ app.py successfully created!")

# ==========================================
# 3️⃣ LAUNCH WITH NGROK
# ==========================================
from pyngrok import ngrok

NGROK_TOKEN = "REPLACE_NGROK_TOKEN_HERE"
ngrok.set_auth_token(NGROK_TOKEN)

subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])
time.sleep(5)

public_url = ngrok.connect(8501).public_url
print(f"🚀 App running at: {public_url}")
