# 🏛️🎓 Harvard's-Artifacts-Collection-ETL-SQL-Analytics-Streamlit-Showcase
An end-to-end data engineering project that extracts, transforms, and loads Harvard Art Museums data into a cloud database, enabling interactive SQL analytics through a Streamlit-based web application.

# 📘 Table of Contents

- Overview

- Key Features

- System Architecture

- Tech Stack

- Database Schema

- Application Workflow

- SQL Analytics (30 Queries)

- Project Setup

- Running the Application

- Author

# 📌 Overview

This project implements a complete ETL pipeline for cultural heritage data sourced from the Harvard Art Museums API.
Artifacts are fetched classification-wise (Photographs, Prints, Sculpture, Paintings, Drawings), normalized into structured tables, and stored securely in TiDB Cloud.

A Streamlit-based user interface allows users to:

1.Extract artifact data from the API

2.Migrate processed data into a relational database

3.Run predefined analytical SQL queries interactively

4.View query results directly inside the application

The project focuses on data engineering, database design, and SQL analytics, rather than visualization.

# 🚀 Key Features

- API-driven ingestion of 12,500+ artifacts

- Classification-wise extraction (2,500 records per classification)

- ETL pipeline for:

- Artifact metadata

- Media attributes

- Color and hue information

- TiDB Cloud (MySQL-compatible) database integration with SSL

- Duplicate-safe bulk insert operations

Streamlit UI for:

- Data extraction

- Database migration

- SQL query execution

- 30 curated analytical SQL queries

- Live tabular previews of extracted data

# 🏗️ System Architecture
 
 Harvard Art Museums API
        ↓
Python ETL Pipeline
        ↓
Data Normalization
        ↓
TiDB Cloud (MySQL)
        ↓
Streamlit Application
        ↓
Interactive SQL Analytics

# 🧰 Tech Stack

👉Programming & Data

👉Python

👉Requests

👉Pandas

👉Database

👉TiDB Cloud (MySQL-compatible)

👉SQL

👉SQLAlchemy

👉PyMySQL

👉Application Layer

👉Streamlit

👉streamlit-option-menu

👉Ngrok (public app access)

👉API

👉Harvard Art Museums API

# 🗄️ Database Schema
1️⃣ metadata

Stores core artifact information.

1.id (Primary Key)

2.title

3.culture

4.period

5.century

6.medium

7.dimensions

8.description

9.department

10.classification

11.accessionyear

12.accessionmethod

2️⃣ media

Stores media-related attributes.

1.objid (Primary Key, FK → metadata.id)

2.imagecount

3.mediacount

4.colorcount

5.db_rank

6.datebegin

7.dateend

3️⃣ colors

Stores color and hue information.

1.objid (FK → metadata.id)

2.color

3.spectrum

4.hue

5.percent

6.css3

# 🧭 Application Workflow

👉Select artifact classification(s)

👉Fetch data from Harvard Art Museums API

👉Normalize records into Metadata, Media, and Colors

👉Preview extracted data inside Streamlit

👉Create database and tables in TiDB Cloud

👉Migrate processed data into SQL tables

👉Execute analytical SQL queries

👉View results in tabular format

# 🧮 SQL Analytics (30 Queries Included)

- The application includes ready-to-run SQL queries covering:

- Century-based artifact analysis

- Culture and classification insights

- Media and image statistics

- Color and hue analysis

- Ranking and accession trends

- Multi-table joins across metadata, media, and colors

- All queries are selectable and executable directly from the UI.

## 📸 Application Screenshots

### Streamlit Dashboard
![Streamlit UI](https://github.com/psnaveen001-foce/Harvard-Artifacts-Collection-ETL-SQL-Analytics-Streamlit-Showcase/blob/a855b78c112c6e6e2f10690751b3648ebfb42461/Home_UI.png)

### SQL Migration
![SQL Migration](https://github.com/psnaveen001-foce/Harvard-Artifacts-Collection-ETL-SQL-Analytics-Streamlit-Showcase/blob/6b27412ea71ccf8830aec848d2b4356cb09ab290/SQL_UI.png)

### SQL Analytics
![SQL Queries](https://github.com/psnaveen001-foce/Harvard-Artifacts-Collection-ETL-SQL-Analytics-Streamlit-Showcase/blob/c1a37a9d9d0c8d0071cda142c137bd8fe4d73842/Analytics.png)


# ⚙️ Setup Instructions
1️⃣ Clone the Repository

```bash
 git clone https://github.com/your-username/Harvard-Artifacts-ETL-Streamlit.git cd Harvard-Artifacts-ETL-Streamlit
```
  
2️⃣ Install Dependencies

```bash
 pip install -r requirements.txt
```

3️⃣ Configure Credentials

- Update the following placeholders in app.py:
  
```bash
API_KEY = "YOUR_HARVARD_API_KEY"
DB_PASSWORD = "YOUR_DATABASE_PASSWORD"
```

▶️ Running the Application
```bash
 streamlit run app.py
```
- The Streamlit app launches locally and provides tabs for:

Data Extraction

Database Migration

SQL Queries

# 👨‍💻 Author

P S Naveen Kumar
Data Engineering • ETL Pipelines • SQL Analytics • API Integrations


