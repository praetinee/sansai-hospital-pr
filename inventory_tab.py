import streamlit as st
import pandas as pd

def to_float(val):
    """ฟังก์ชันช่วยแปลงค่าในตารางให้เป็นตัวเลข (ป้องกัน error จากลูกน้ำหรือช่องว่าง)"""
    if pd.isna(val): 
        return 0.0
    val_str = str(val).strip().replace(',', '')
    if val_str.lower() in ['', '-', 'nan', 'none']: 
        return 0.0
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def load_and_process_inventory(file_path, item_column_name):
    """ฟังก์ชันอ่านข้อมูลแบบ Manual Parsing ป้องกันปัญหาโครงสร้าง CSV เหลื่อมล้ำ"""
    try:
        # 1. ใช้ names=range(100) กางข้อมูลทั้งหมดเป็นตารางดิบๆ ตัดปัญหา Error ตอนโหลด
        df_raw = pd.read_csv(file_path, names=range(100), encoding='utf-8-sig', dtype=str)
        
        # 2. ค้นหาบรรทัดที่เป็น "วันที่" (แถวที่ 2 ในภาพของคุณ)
        date_row_idx = -1
        for i, row in df_raw.iterrows():
            row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
            if 'วันที่' in row_str:
                # ถ้าเจอบรรทัดคำว่า "วันที่" แปลว่าบรรทัด 'ถัดไป' คือ 8 มี.ค., 9 มี.ค.
                date_row_idx = i + 1 
                break
                
        # หากไม่เจอ ให้ใช้วิธีสำรอง สแกนหาชื่อเดือน
        if date_row_idx == -1:
            thai_months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
            for i, row in df_raw.iterrows():
                row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
                if any(month in row_str for month in thai_months):
                    date_row_idx = i
                    break

        if date_row_idx == -1 or date_row_idx >= len(df_raw):
            return None, None, None

        # 3. ดึงบรรทัดที่มีวันที่จริงๆ ออกมาใช้งาน (บรรทัดที่ 3)
        raw_dates = df_raw.iloc[date_row_idx]
        
        valid_col_indices = [0] # index 0 บังคับเป็นชื่อรายการเสมอ
        date_columns = []
        
        # วนลูปเก็บเฉพาะคอลัมน์ที่มีวันที่ (ข้ามคอลัมน์แรกที่เป็นชื่อรายการ/ช่องว่าง)
        for i in range(1, len(raw_dates)):
            col_val = str(raw_dates[i]).strip()
            if pd.notna(raw_dates[i]) and col_val.lower() not in ['nan', 'none', '']:
                date_columns.append(col_val)
                valid_col_indices.append(i)

        if not date_columns:
            return None, None, None

        # 4. ตัดเฉพาะข้อมูลรายการและวันที่ โดยเริ่มเอาตั้งแต่บรรทัด "ใต้" วันที่ลงไป
        df = df_raw.iloc[date_row_idx + 1:, valid_col_indices].copy()
        df.columns = [item_column_name] + date_columns
            
        # 5. ทำความสะอาดข้อมูล: ลบแถวที่ชื่อรายการเป็นค่าว่าง
        df = df.dropna(subset=[item_column_name])
        df = df[df[item_column_name].astype(str).str.strip().str.lower() != 'nan']
        df = df[df[item_column_name].astype(str).str.strip() != '']
        
        latest_date = None
        valid_date_cols = []
        
        # 6. หาวันที่ล่าสุดที่มีข้อมูลตัวเลขกรอกไว้ (สแกนจากขวามาซ้าย)
        for col in reversed(date_columns):
            has_data = False
            for val in df[col]:
                val_str = str(val).strip().replace(',', '')
                if pd.notna(val) and val_str not in ['', 'nan', 'None', '-']:
                    try:
                        float(val_str)
                        has_data = True
                        break
                    except ValueError:
                        pass
            if has_data:
                latest_date = col
                break
                
        # หากพบวันที่ล่าสุด จะเก็บข้อมูลตั้งแต่วันแรกถึงวันล่าสุดเพื่อใช้สร้างกราฟ
        if latest_date:
            for col in date_columns:
                valid_date_cols.append(col)
                if col == latest_date:
                    break
                    
        return df, latest_date, valid_date_cols
        
    except FileNotFoundError:
        st.error(f"⚠️ ไม่พบไฟล์: {file_path}")
        return None, None, None
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาดในการอ่านข้อมูล: {e}")
        return None, None, None

def display_modern_inventory_table(df, item_col, latest_date, valid_date_cols):
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบมีกราฟเส้น (Sparkline)"""
    if df is None or df.empty or not latest_date:
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบการตั้งค่าไฟล์ CSV")
        return

    display_df = pd.DataFrame()
    display_df['รายการ'] = df[item_col]
    
    # แปลงข้อมูลวันล่าสุดเป็นตัวเลขเพื่อแสดงผล
    display_df['คงเหลือล่าสุด'] = df[latest_date].apply(to_float).astype(int)
    
    history_data = []
    for index, row in df.iterrows():
        hist = [to_float(x) for x in row[valid_date_cols].values]
        history_data.append(hist)
        
    display_df['ประวัติย้อนหลัง'] = history_data

    st.dataframe(
        display_df,
        column_config={
            "รายการ": st.column_config.TextColumn("📝 ชื่อรายการ", width="large"),
            "คงเหลือล่าสุด": st.column_config.NumberColumn(
                f"📦 จำนวนคงเหลือ ณ {latest_date}",
                help="ข้อมูลอัปเดตล่าสุด",
                format="%d",
            ),
            "ประวัติย้อนหลัง": st.column_config.LineChartColumn(
                "📈 แนวโน้มการเบิกจ่าย (ย้อนหลัง)",
                help=f"กราฟแสดงการเปลี่ยนแปลงตั้งแต่วันแรกถึง {latest_date}"
            )
        },
        hide_index=True,
        use_container_width=True
    )

def render_inventory_ui():
    """ฟังก์ชันหลักสำหรับให้ app.py ดึงไปแสดงผล"""
    st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
    st.markdown("แสดงข้อมูลจำนวนคงคลัง **เฉพาะข้อมูลล่าสุด** พร้อมกราฟแนวโน้มย้อนหลังเพื่อให้ดูง่ายและสบายตา")
    st.divider()

    med_supplies_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
    medicines_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

    # ประมวลผลแต่ละไฟล์
    df_sup, latest_date_sup, valid_cols_sup = load_and_process_inventory(med_supplies_file, "รายการพัสดุการแพทย์")
    df_med, latest_date_med, valid_cols_med = load_and_process_inventory(medicines_file, "รายการยา")

    latest_update = latest_date_sup if latest_date_sup else "ไม่มีข้อมูล"
    st.info(f"🔄 **อัปเดตข้อมูลล่าสุดเมื่อ:** {latest_update}")

    tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

    with tab_sup:
        display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", latest_date_sup, valid_cols_sup)

    with tab_med:
        display_modern_inventory_table(df_med, "รายการยา", latest_date_med, valid_cols_med)
