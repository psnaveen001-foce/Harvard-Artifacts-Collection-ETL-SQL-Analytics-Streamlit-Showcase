#from  app.py

# ==========================================
# TAB 3: SQL QUERIES
# ==========================================
if selected == "SQL Queries":
    st.subheader("🔎 Analytical SQL Queries")

    queries = {
        "#1 List all artifacts from 11th century Byzantine culture": "SELECT id, title, culture, century, period, classification FROM metadata WHERE century='11th century' AND culture='Byzantine';",
        "#2 Unique cultures represented in the artifacts": "SELECT DISTINCT culture FROM metadata WHERE culture IS NOT NULL;",
        "#3 List all artifacts from the Archaic Period": "SELECT * FROM metadata WHERE period='Archaic period';",
        "#4 Artifact titles ordered by accession year descending": "SELECT title, accessionyear FROM metadata WHERE accessionyear IS NOT NULL ORDER BY accessionyear DESC;",
        "#5 Count of artifacts per department": "SELECT department, COUNT(*) as count FROM metadata GROUP BY department;",
        "#6 Artifacts with more than 1 image": "SELECT m.title, me.imagecount FROM media me JOIN metadata m ON m.id=me.objid WHERE me.imagecount>1;",
        "#7 Average rank of all artifacts": "SELECT AVG(db_rank) as average_rank FROM media;",
        "#8 Artifacts with higher colorcount than mediacount": "SELECT objid, colorcount, mediacount FROM media WHERE colorcount>mediacount;",
        "#9 Artifacts created between 1500 and 1600": "SELECT objid, datebegin, dateend FROM media WHERE datebegin IS NOT NULL  AND dateend IS NOT NULL  AND datebegin <> 0  AND dateend <> 0  AND datebegin >= 1500  AND dateend <= 1600;",
        "#10 Count of artifacts with no media files": "SELECT COUNT(*) as no_media_count FROM media WHERE mediacount=0;",
        "#11 Distinct hues used in the dataset": "SELECT DISTINCT hue FROM colors;",
        "#12 Top 5 most used colors by frequency": "SELECT color, COUNT(*) as count FROM colors GROUP BY color ORDER BY COUNT(*) DESC LIMIT 5;",
        "#13 Average coverage percentage for each hue": "SELECT hue, AVG(percent) as avg_coverage FROM colors GROUP BY hue;",
        "#14 List all colors used for a given artifact Object ID (Dynamic)": "SELECT * FROM colors WHERE objid=58203;",
        "#15 total number of color entries in the dataset": "SELECT COUNT(*) as total_colors FROM colors;",
        "#16 List artifact titles and hues for all artifacts belonging to the Byzantine culture": "SELECT DISTINCT m.title, c.hue FROM metadata m JOIN colors c ON m.id=c.objid WHERE culture='Byzantine';",
        "#17 List each artifact title with its associated hues(Distinct):": "SELECT m.title, GROUP_CONCAT(DISTINCT c.hue) as hues FROM metadata m JOIN colors c ON m.id=c.objid GROUP BY m.id;",
        "#18 Get artifact titles, cultures, and media ranks where the period is not null": "SELECT m.title, m.culture, me.db_rank FROM metadata m JOIN media me ON m.id=me.objid WHERE m.period IS NOT NULL;",
        "#19 Find artifact titles ranked in the top 10 that include the color hue Grey": "SELECT DISTINCT m.title, me.db_rank FROM metadata m JOIN media me ON m.id = me.objid JOIN colors c ON m.id = c.objid WHERE c.hue = 'Grey' ORDER BY me.db_rank ASC LIMIT 10;;",
        "#20  How many artifacts exist per classification, and what is the average media count for each": "SELECT m.classification, COUNT(*) as count, AVG(me.mediacount) as avg_media FROM metadata m JOIN media me ON m.id=me.objid GROUP BY m.classification;",
        "#21 Artifacts with silver medium": "SELECT DISTINCT title, medium FROM metadata WHERE medium IS NOT NULL AND LOWER(medium) LIKE '%%silver%%';",
        "#22 Artifacts acquired via donation": "SELECT title FROM metadata WHERE accessionmethod='Gift';",
        "#23 Artifact count per century": "SELECT century, COUNT(*) AS artifact_count FROM metadata WHERE century IS NOT NULL AND century <> 'Unidentified' GROUP BY century ORDER BY artifact_count DESC;",
        "#24 Longest artifact title": "SELECT title, LENGTH(title) as len FROM metadata ORDER BY LENGTH(title) DESC LIMIT 1;",
        "#25 List artifacts with their classification and accession year": "SELECT title, classification, accessionyear FROM metadata WHERE accessionyear IS NOT NULL ORDER BY accessionyear;",
        "#26 Artifacts with at least one image": "SELECT m.title FROM metadata m JOIN media me ON m.id=me.objid WHERE me.imagecount>0;",
        "#27 Hue with highest avg coverage": "SELECT hue, AVG(percent) as coverage FROM colors GROUP BY hue ORDER BY AVG(percent) DESC LIMIT 1;",
        "#28 Artifacts with Red and Blue hues": "SELECT objid FROM colors WHERE hue IN ('Red','Blue') GROUP BY objid HAVING COUNT(DISTINCT hue)=2;",
        "#29 Artifact titles with media rank and total colors": "SELECT m.title, me.db_rank, COUNT(c.color) AS total_colors FROM metadata m JOIN media me ON m.id = me.objid LEFT JOIN colors c ON m.id = c.objid GROUP BY m.id, m.title, me.db_rank ORDER BY me.db_rank ASC;",
        "#30 Top 10 artifacts with highest image count": "SELECT m.title, me.imagecount FROM metadata m JOIN media me ON m.id=me.objid ORDER BY me.imagecount DESC LIMIT 10;"
    }

    selected_query_name = st.selectbox("Select a Query to Run", list(queries.keys()))

    # Logic for Dynamic Query #14
    if selected_query_name.startswith("#14"):
        user_obj_id = st.text_input("Enter Object ID to search:", value="58203")
        # Update the query string dynamically based on user input
        sql_query = f"SELECT * FROM colors WHERE objid={user_obj_id};"
    else:
        sql_query = queries[selected_query_name]

    st.code(sql_query, language="sql")

    if st.button("Run SQL Query"):
        try:
            engine_target = create_engine(DB_CONNECTION_STR_TARGET)
            with engine_target.connect() as conn:
                df = pd.read_sql(sql_query, conn)
                st.dataframe(df)
        except Exception as e:
            st.error(f"Query Failed: {e}")
