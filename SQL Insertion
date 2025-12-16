from app.py

# ==========================================
# TAB 1: DATA EXTRACTION
# ==========================================
if selected == "Data Extraction":
    st.subheader("📥 Fetch Artifacts from API")

    # Define available classifications
    base_classifications = ["Photographs", "Prints", "Sculpture", "Paintings", "Drawings"]

    # Dropdown for Classification Selection
    selected_cls_option = st.selectbox(
        "Select Classification to Fetch",
        ["Fetch All"] + base_classifications
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_btn = st.button("🚀 Start Extraction")

    if fetch_btn:
        st.session_state.all_records = [] # reset
        st.session_state.metadata = []
        st.session_state.media = []
        st.session_state.colors = []

        # Determine which classifications to fetch
        if selected_cls_option == "Fetch All":
            target_classifications = base_classifications
        else:
            target_classifications = [selected_cls_option]

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Dynamic total steps based on selection
        total_steps = len(target_classifications) * 25
        current_step = 0
        start_time = time.time()

        for classification in target_classifications:
            for page in range(1, 26):
                status_text.text(f"Fetching: {classification} | Page {page}/25...")
                try:
                    params = {
                        "apikey": API_KEY,
                        "size": 100,
                        "page": page,
                        "classification": classification
                    }
                    r = requests.get(BASE_URL, params=params)
                    r.raise_for_status()
                    data = r.json()
                    records = data.get("records", [])
                    st.session_state.all_records.extend(records)

                    # Process tables
                    for rcd in records:
                        oid = rcd.get("id")
                        if not oid:
                            continue
                        st.session_state.metadata.append({
                            "id": oid, "title": rcd.get("title"), "culture": rcd.get("culture"),
                            "period": rcd.get("period"), "century": rcd.get("century"),
                            "medium": rcd.get("medium"), "dimensions": rcd.get("dimensions"),
                            "description": rcd.get("description"), "department": rcd.get("department"),
                            "classification": rcd.get("classification"), "accessionyear": rcd.get("accessionyear"),
                            "accessionmethod": rcd.get("accessionmethod")
                        })
                        st.session_state.media.append({
                            "objid": oid, "imagecount": rcd.get("imagecount"),
                            "mediacount": rcd.get("mediacount"), "colorcount": rcd.get("colorcount"),
                            "db_rank": rcd.get("rank"), "datebegin": rcd.get("datebegin"), "dateend": rcd.get("dateend")
                        })
                        for c in rcd.get("colors") or []:
                            st.session_state.colors.append({
                                "objid": oid, "color": c.get("color"), "spectrum": c.get("spectrum"),
                                "hue": c.get("hue"), "percent": c.get("percent"), "css3": c.get("css3")
                            })

                except Exception as e:
                    st.error(f"Error: {e}")

                current_step += 1
                progress_bar.progress(min(current_step / total_steps, 1.0))

        st.session_state.data_fetched = True
        duration = round(time.time() - start_time, 2)
        status_text.empty()
        st.success(f"✅ Extraction Complete! Fetched {len(st.session_state.all_records)} records in {duration}s.")

    # Preview tables
    if st.session_state.data_fetched:
        st.divider()
        st.subheader("📋 Metadata Table (100 sample records)")
        st.dataframe(pd.DataFrame(st.session_state.metadata[:100]))
        st.subheader("🖼️ Media Table (100 sample records)")
        st.dataframe(pd.DataFrame(st.session_state.media[:100]))
        st.subheader("🎨 Colors Table (100 sample records)")
        st.dataframe(pd.DataFrame(st.session_state.colors[:100]))

# ==========================================
# TAB 2: MIGRATE TO SQL
# ==========================================
if selected == "Migrate to SQL":
    st.subheader("🗄️ Database Migration (TiDB)")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Records ready to upload: {len(st.session_state.all_records)}")

    if st.button("🔄 Create DB & Upload Data"):
        if not st.session_state.data_fetched or not st.session_state.all_records:
            st.error("⚠️ No data found! Fetch data first.")
        else:
            status_box = st.status("Processing Database Operations...", expanded=True)
            try:
                # Connect root and create DB
                status_box.write("🔌 Connecting to TiDB Root...")
                engine_root = create_engine(DB_CONNECTION_STR_ROOT)
                with engine_root.begin() as conn:
                    conn.execute(text("CREATE DATABASE IF NOT EXISTS Naveen_Harvard_Artifacts_1;"))
                status_box.write("✅ Database checked/created.")

                engine_target = create_engine(DB_CONNECTION_STR_TARGET)

                # Create tables
                status_box.write("🏗️ Creating Tables...")
                with engine_target.begin() as conn:
                    conn.execute(text(\"\"\"
                        CREATE TABLE IF NOT EXISTS metadata (
                            id INT PRIMARY KEY, title TEXT, culture TEXT, period TEXT, century TEXT,
                            medium TEXT, dimensions TEXT, description TEXT, department TEXT,
                            classification TEXT, accessionyear INT, accessionmethod TEXT
                        );
                    \"\"\"))
                    conn.execute(text(\"\"\"
                        CREATE TABLE IF NOT EXISTS media (
                            objid INT PRIMARY KEY, imagecount INT, mediacount INT, colorcount INT,
                            db_rank INT, datebegin INT, dateend INT, FOREIGN KEY (objid) REFERENCES metadata(id)
                        );
                    \"\"\"))
                    conn.execute(text(\"\"\"
                        CREATE TABLE IF NOT EXISTS colors (
                            objid INT, color TEXT, spectrum TEXT, hue TEXT, percent FLOAT, css3 TEXT,
                            FOREIGN KEY (objid) REFERENCES metadata(id)
                        );
                    \"\"\"))

                # Bulk insert
                status_box.write("📤 Uploading Data...")
                with engine_target.begin() as conn:
                    if st.session_state.metadata:
                        conn.execute(text(
                            "INSERT IGNORE INTO metadata VALUES (:id, :title, :culture, :period, :century, :medium, :dimensions, :description, :department, :classification, :accessionyear, :accessionmethod)"
                        ), st.session_state.metadata)
                    if st.session_state.media:
                        conn.execute(text(
                            "INSERT IGNORE INTO media VALUES (:objid, :imagecount, :mediacount, :colorcount, :db_rank, :datebegin, :dateend)"
                        ), st.session_state.media)
                    if st.session_state.colors:
                        conn.execute(text(
                            "INSERT INTO colors VALUES (:objid, :color, :spectrum, :hue, :percent, :css3)"
                        ), st.session_state.colors)

                status_box.update(label="✅ Migration Successful!", state="complete", expanded=False)
                st.success("Data successfully uploaded to TiDB Cloud.")
            except Exception as e:
                status_box.update(label="❌ Migration Failed", state="error")
                st.error(f"Database Error: {e}")
