import streamlit as st
import pandas as pd
import re

def get_gsheet_csv_url(url_or_path):
    """แปลง URL ของ Google Sheet เป็นลิงก์ดาวน์โหลด CSV อัตโนมัติ"""
    if isinstance(url_or_path, str) and "docs.google.com/spreadsheets" in url_or_path:
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', url_or_path)
        gid_match = re.search(r'gid=([0-9]+)', url_or_path)
        if match:
            sheet_id = match.group(1)
            gid = gid_match.group(1) if gid_match else "0"
            return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return url_or_path

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

@st.cache_data(ttl=300) # แคชข้อมูล 5 นาที เพื่อไม่ให้โหลด Google Sheet ถี่เกินไป
def load_and_process_inventory(source_url, item_column_name):
    """ฟังก์ชันอ่านข้อมูลจาก Google Sheet เจาะทะลุหาแถวที่ 2 และ 3 อัตโนมัติ"""
    try:
        # แปลงลิงก์ และโหลดข้อมูลกางเป็นตารางดิบ
        csv_url = get_gsheet_csv_url(source_url)
        df_raw = pd.read_csv(csv_url, names=range(100), header=None, encoding='utf-8-sig', dtype=str)
        
        # 1. สแกนหาแถวที่มีคำว่า "วันที่" หรือ "รายการ" (ซึ่งก็คือแถวที่ 2 ในภาพของคุณ)
        header_row_idx = -1
        for i, row in df_raw.iterrows():
            row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
            if 'วันที่' in row_str or 'รายการ' in row_str or 'ยา' in row_str:
                header_row_idx = i
                break
                
        if header_row_idx == -1 or header_row_idx + 1 >= len(df_raw):
            return None, None, None

        # 2. แถวถัดไป (แถวที่ 3) คือแถวที่มีข้อมูล "8 มี.ค.", "9 มี.ค." ฯลฯ
        date_row_idx = header_row_idx + 1
        dates = df_raw.iloc[date_row_idx].values
        
        valid_col_indices = [0] # บังคับเก็บคอลัมน์ 0 (รายชื่อเวชภัณฑ์) เสมอ
        date_columns = []
        
        # วนลูปเก็บเฉพาะคอลัมน์ที่มีข้อมูลวันที่จริงๆ (ข้ามช่องว่าง)
        for i in range(1, len(dates)):
            val = str(dates[i]).strip()
            if pd.notna(dates[i]) and val.lower() not in ['nan', 'none', '']:
                date_columns.append(val)
                valid_col_indices.append(i)

        if not date_columns:
            return None, None, None

        # 3. ตัดเอาเฉพาะข้อมูลส่วนล่างสุด (ตั้งแต่บรรทัดที่ 4 เป็นต้นไป)
        df = df_raw.iloc[date_row_idx + 1:, valid_col_indices].copy()
        df.columns = [item_column_name] + date_columns
            
        # ทำความสะอาดแถวว่าง
        df = df.dropna(subset=[item_column_name])
        df = df[df[item_column_name].astype(str).str.strip().str.lower() != 'nan']
        df = df[df[item_column_name].astype(str).str.strip() != '']
        
        # 4. หาวันที่ล่าสุดที่มีคนพิมพ์ตัวเลขลงไป
        latest_date = None
        valid_date_cols = []
        
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
                
        if latest_date:
            for col in date_columns:
                valid_date_cols.append(col)
                if col == latest_date:
                    break
                    
        return df, latest_date, valid_date_cols
        
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheet: {e}")
        return None, None, None

def display_modern_inventory_table(df, item_col, latest_date, valid_date_cols):
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบมีกราฟเส้น (Sparkline)"""
    if df is None or df.empty or not latest_date:
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบลิงก์ Google Sheet")
        return

    display_df = pd.DataFrame()
    display_df['รายการ'] = df[item_col]
    
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
    st.markdown("ดึงข้อมูลตรงจาก **Google Sheets** แสดงเฉพาะยอดล่าสุดพร้อมกราฟย้อนหลัง")
    st.divider()

    # นำ URL จากที่คุณส่งมาใส่ไว้ให้ทำงานได้ทันที!
    med_supplies_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=38922931#gid=38922931"
    
    # อัปเดตชีตยาเป็นลิงก์ล่าสุด
    medicines_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=50246944#gid=50246944"

    # ประมวลผลแต่ละไฟล์
    df_sup, latest_date_sup, valid_cols_sup = load_and_process_inventory(med_supplies_sheet, "รายการพัสดุการแพทย์")
    df_med, latest_date_med, valid_cols_med = load_and_process_inventory(medicines_sheet, "รายการยา")

    latest_update = latest_date_sup if latest_date_sup else "ไม่มีข้อมูล"
    st.info(f"🔄 **อัปเดตข้อมูลล่าสุดเมื่อ:** {latest_update}")

    tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

    with tab_sup:
        display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", latest_date_sup, valid_cols_sup)

    with tab_med:
        display_modern_inventory_table(df_med, "รายการยา", latest_date_med, valid_cols_med)
