-- ==========================================
-- DATABASE: Harvard Artifacts
-- TABLE CREATION SCRIPT
-- ==========================================

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

CREATE TABLE IF NOT EXISTS colors (
    objid INT,
    color TEXT,
    spectrum TEXT,
    hue TEXT,
    percent FLOAT,
    css3 TEXT,
    FOREIGN KEY (objid) REFERENCES metadata(id)
);

-- ==========================================
-- DATA INSERTION QUERIES
-- ==========================================

-- Metadata
INSERT IGNORE INTO metadata
VALUES (
    :id,
    :title,
    :culture,
    :period,
    :century,
    :medium,
    :dimensions,
    :description,
    :department,
    :classification,
    :accessionyear,
    :accessionmethod
);

-- Media
INSERT IGNORE INTO media
VALUES (
    :objid,
    :imagecount,
    :mediacount,
    :colorcount,
    :db_rank,
    :datebegin,
    :dateend
);

-- Colors
INSERT INTO colors
VALUES (
    :objid,
    :color,
    :spectrum,
    :hue,
    :percent,
    :css3
);

## Python Execution Block:

from sqlalchemy import create_engine, text

engine = create_engine(DB_CONNECTION_STRING)

with engine.begin() as conn:
    conn.execute(
        text("""INSERT IGNORE INTO metadata VALUES
        (:id, :title, :culture, :period, :century, :medium,
         :dimensions, :description, :department, :classification,
         :accessionyear, :accessionmethod)"""),
        metadata_data
    )

    conn.execute(
        text("""INSERT IGNORE INTO media VALUES
        (:objid, :imagecount, :mediacount, :colorcount,
         :db_rank, :datebegin, :dateend)"""),
        media_data
    )

    conn.execute(
        text("""INSERT INTO colors VALUES
        (:objid, :color, :spectrum, :hue, :percent, :css3)"""),
        colors_data
    )
