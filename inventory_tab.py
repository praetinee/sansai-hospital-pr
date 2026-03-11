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

def parse_value(val):
    """ฟังก์ชันแปลงค่าเป็นตัวเลข (แยกระหว่างช่องว่าง กับเลข 0)"""
    # ถ้าไม่ได้กรอก (ช่องว่าง) ให้คืนค่า None เพื่อใช้ในการเช็ควันล่าสุด
    if pd.isna(val): 
        return None
    val_str = str(val).strip().replace(',', '')
    if val_str.lower() in ['', '-', 'nan', 'none']: 
        return None
    try:
        return float(val_str)
    except ValueError:
        return None

@st.cache_data(ttl=300) # แคชข้อมูล 5 นาที เพื่อไม่ให้โหลด Google Sheet ถี่เกินไป
def load_and_process_inventory(source_url, item_column_name):
    """ฟังก์ชันอ่านข้อมูลจาก Google Sheet โดยสแกนหาแถวที่มีวันที่ (แถว 3) อัตโนมัติ"""
    try:
        # แปลงลิงก์ และโหลดข้อมูลกางเป็นตารางดิบ
        csv_url = get_gsheet_csv_url(source_url)
        df_raw = pd.read_csv(csv_url, names=range(100), header=None, encoding='utf-8-sig', dtype=str)
        
        # 1. สแกนหาบรรทัดที่เป็น "วันที่" (แถวที่ 3) โดยเช็คจากชื่อเดือนภาษาไทย
        thai_months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
        date_row_idx = -1
        
        for i, row in df_raw.iterrows():
            # นับว่าบรรทัดนี้มีคอลัมน์ที่มีชื่อเดือนกี่คอลัมน์
            month_match_count = sum(1 for cell in row.values if pd.notna(cell) and any(m in str(cell) for m in thai_months))
            # ถ้ามีชื่อเดือนโผล่มาตั้งแต่ 2 คอลัมน์ขึ้นไป ถือว่าเป็นบรรทัดวันที่แน่นอน (แถวที่ 3)
            if month_match_count >= 2: 
                date_row_idx = i
                break
                
        if date_row_idx == -1:
            return None, None

        # 2. ดึงข้อมูลจากแถววันที่เจอ (แถวที่ 3)
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
            return None, None

        # 3. ตัดเอาเฉพาะข้อมูลส่วนล่างสุด (ตั้งแต่บรรทัดที่ 4 เป็นต้นไป)
        df = df_raw.iloc[date_row_idx + 1:, valid_col_indices].copy()
        df.columns = [item_column_name] + date_columns
            
        # ทำความสะอาดแถวว่าง
        df = df.dropna(subset=[item_column_name])
        df = df[df[item_column_name].astype(str).str.strip().str.lower() != 'nan']
        df = df[df[item_column_name].astype(str).str.strip() != '']
        
        return df, date_columns
        
    except Exception as e:
        st.error(f"⚠️ เกิดข้อผิดพลาดในการดึงข้อมูลจาก Google Sheet: {e}")
        return None, None

def display_modern_inventory_table(df, item_col, date_columns):
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบ 3 คอลัมน์ที่กระชับและเข้าใจง่าย"""
    if df is None or df.empty or not date_columns:
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบลิงก์ Google Sheet")
        return

    # 1. หาวันที่ล่าสุดจากภาพรวมของทั้งตาราง (เพื่อใช้ตั้งชื่อคอลัมน์ Header)
    global_latest_date = date_columns[-1] if date_columns else "ล่าสุด"
    for col in reversed(date_columns):
        # เช็คว่ามีใครกรอกข้อมูลในคอลัมน์นี้บ้างไหม ถ้ามีให้ใช้วันนี้เป็นวันล่าสุด
        if any(parse_value(val) is not None for val in df[col]):
            global_latest_date = col
            break

    # สร้างชื่อคอลัมน์ให้ตรงตามเงื่อนไขที่ขอมา
    stock_col_name = f"คงคลัง ณ วันที่ {global_latest_date}"
    change_col_name = "การเพิ่มขึ้น/ลดลง (จากข้อมูลล่าสุด)"

    processed_rows = []
    
    # 2. วนลูปเช็คข้อมูลทีละไอเทม
    for index, row in df.iterrows():
        item_name = row[item_col]
        
        valid_points = []
        
        # เก็บเฉพาะค่าตัวเลขที่ถูกกรอกไว้จริงของไอเทมนั้นๆ
        for col in date_columns:
            val = parse_value(row[col])
            if val is not None:
                valid_points.append(val)

        current_val = 0
        delta_str = "-"

        # หากมีการกรอกข้อมูลมาแล้วอย่างน้อย 1 วัน
        if len(valid_points) > 0:
            current_val = valid_points[-1] # ยอดล่าสุดที่มีการกรอก
            
            # หากมีการกรอกมาแล้ว 2 วันขึ้นไป ให้เอามาเทียบส่วนต่าง
            if len(valid_points) > 1:
                prev_val = valid_points[-2]
                diff = current_val - prev_val
                
                # จัด Format ให้ดูทันสมัย สวยงาม และเข้าใจง่ายขึ้น พร้อมใส่ลูกน้ำ
                if diff > 0:
                    delta_str = f"🔺 +{int(diff):,}"
                elif diff < 0:
                    delta_str = f"🔻 {int(diff):,}"
                else:
                    delta_str = "➖ 0"
            else:
                # เพิ่งกรอกวันแรก
                delta_str = "➖ 0"

        processed_rows.append({
            "ชื่อรายการ": item_name,
            stock_col_name: int(current_val) if valid_points else 0,
            change_col_name: delta_str
        })

    display_df = pd.DataFrame(processed_rows)

    # 3. แสดงผลตาราง (ใช้ 3 คอลัมน์หลักตามที่กำหนดเป๊ะ)
    st.dataframe(
        display_df,
        column_config={
            "ชื่อรายการ": st.column_config.TextColumn(
                "📝 ชื่อรายการ", 
                width="large"
            ),
            stock_col_name: st.column_config.NumberColumn(
                f"📦 {stock_col_name}", 
                format="%d",
                width="medium"
            ),
            change_col_name: st.column_config.TextColumn(
                f"📊 {change_col_name}", 
                width="medium"
            )
        },
        hide_index=True,
        use_container_width=True
    )

def render_inventory_ui():
    """ฟังก์ชันหลักสำหรับให้ app.py ดึงไปแสดงผล"""
    st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
    st.markdown("ดึงข้อมูลตรงจาก **Google Sheets** โดยระบบจะประมวลผล **วันที่อัปเดตล่าสุด** และ **ยอดเปรียบเทียบจากวันก่อนหน้า** ให้โดยอัตโนมัติ")
    st.divider()

    # ลิงก์จาก Google Sheet
    med_supplies_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=38922931#gid=38922931"
    medicines_sheet = "https://docs.google.com/spreadsheets/d/1-WhGMaME7Gbe7o6V4_rtbrqxCZSX4Bfnsz-siOV9T4Q/edit?gid=50246944#gid=50246944"

    # ประมวลผลตาราง
    df_sup, cols_sup = load_and_process_inventory(med_supplies_sheet, "รายการพัสดุการแพทย์")
    df_med, cols_med = load_and_process_inventory(medicines_sheet, "รายการยา")

    tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

    with tab_sup:
        display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", cols_sup)

    with tab_med:
        display_modern_inventory_table(df_med, "รายการยา", cols_med)
