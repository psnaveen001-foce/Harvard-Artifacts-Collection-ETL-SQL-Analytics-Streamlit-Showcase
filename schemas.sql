# ---------------------------
️⃣ Create Tables
# ---------------------------
with engine_new.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS metadata (
            id INT PRIMARY KEY,
            title TEXT,
            culture TEXT,
            period TEXT,
            century TEXT,
            medium TEXT,
            dimensions TEXT,
            description TEXT,
            department TEXT,
            classification TEXT,
            accessionyear INT,
            accessionmethod TEXT
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS media (
            objid INT PRIMARY KEY,
            imagecount INT,
            mediacount INT,
            colorcount INT,
            db_rank INT,
            datebegin INT,
            dateend INT,
            FOREIGN KEY (objid) REFERENCES metadata(id)
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS colors (
            objid INT,
            color TEXT,
            spectrum TEXT,
            hue TEXT,
            percent FLOAT,
            css3 TEXT,
            FOREIGN KEY (objid) REFERENCES metadata(id)
        );
    """))
