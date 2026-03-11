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
    """ฟังก์ชันอ่านข้อมูลจาก Google Sheet เจาะทะลุหาแถวที่ 2 และ 3 อัตโนมัติ"""
    try:
        # แปลงลิงก์ และโหลดข้อมูลกางเป็นตารางดิบ
        csv_url = get_gsheet_csv_url(source_url)
        df_raw = pd.read_csv(csv_url, names=range(100), header=None, encoding='utf-8-sig', dtype=str)
        
        # 1. สแกนหาแถวที่มีคำว่า "วันที่" หรือ "รายการ"
        header_row_idx = -1
        for i, row in df_raw.iterrows():
            row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
            if 'วันที่' in row_str or 'รายการ' in row_str or 'ยา' in row_str:
                header_row_idx = i
                break
                
        if header_row_idx == -1 or header_row_idx + 1 >= len(df_raw):
            return None, None

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
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบคำนวณรายบรรทัด (เข้าใจง่าย + มีประวัติ)"""
    if df is None or df.empty or not date_columns:
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบลิงก์ Google Sheet")
        return

    processed_rows = []
    
    # วนลูปเช็คข้อมูล "ทีละบรรทัด (ทีละไอเทม)"
    for index, row in df.iterrows():
        item_name = row[item_col]
        
        valid_points = []
        all_points = []
        
        # สแกนหาวันที่กรอกข้อมูลของไอเทมนี้
        last_valid_val = 0
        for col in date_columns:
            val = parse_value(row[col])
            if val is not None:
                valid_points.append((col, val))
                last_valid_val = val
                all_points.append(val)
            else:
                # กรณีไม่ได้กรอกในวันนั้น ให้ใช้ค่ายอดคงเหลือจากวันก่อนหน้า (Forward fill)
                all_points.append(last_valid_val)

        current_date = "ยังไม่มีข้อมูล"
        current_val = 0
        delta_str = "-"

        # หากมีการกรอกข้อมูลอย่างน้อย 1 วัน
        if len(valid_points) > 0:
            current_date, current_val = valid_points[-1] # วันล่าสุดที่มีการกรอก
            
            # หากมีการกรอกข้อมูลอย่างน้อย 2 วัน (เพื่อนำมาเทียบความต่าง)
            if len(valid_points) > 1:
                prev_date, prev_val = valid_points[-2] # วันก่อนหน้าที่มีการกรอก
                diff = current_val - prev_val
                
                if diff > 0:
                    delta_str = f"🔺 เพิ่มขึ้น {int(diff)} (เทียบ {prev_date})"
                elif diff < 0:
                    delta_str = f"🔻 ลดลง {abs(int(diff))} (เทียบ {prev_date})"
                else:
                    delta_str = f"➖ คงที่ (เทียบ {prev_date})"
            else:
                delta_str = f"เริ่มบันทึก (ข้อมูลแรก)"

        processed_rows.append({
            "รายการ": item_name,
            "อัปเดตล่าสุด": current_date,
            "คงเหลือ": int(current_val),
            "การเปลี่ยนแปลง": delta_str,
            "แนวโน้ม": all_points
        })

    display_df = pd.DataFrame(processed_rows)

    # ตกแต่ง UI ตารางให้สวยงามและอ่านง่าย
    st.dataframe(
        display_df,
        column_config={
            "รายการ": st.column_config.TextColumn("📝 ชื่อรายการ", width="large"),
            "อัปเดตล่าสุด": st.column_config.TextColumn("📅 อัปเดตล่าสุด", width="medium"),
            "คงเหลือ": st.column_config.NumberColumn("📦 คงเหลือ", format="%d"),
            "การเปลี่ยนแปลง": st.column_config.TextColumn("📊 เปลี่ยนแปลง (เทียบวันก่อนหน้า)", width="medium"),
            "แนวโน้ม": st.column_config.LineChartColumn("📈 แนวโน้มยอดคงคลัง")
        },
        hide_index=True,
        use_container_width=True
    )

def render_inventory_ui():
    """ฟังก์ชันหลักสำหรับให้ app.py ดึงไปแสดงผล"""
    st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
    st.markdown("ดึงข้อมูลตรงจาก **Google Sheets** โดยระบบจะประมวลผล **วันที่อัปเดตล่าสุด** และ **ยอดเปรียบเทียบจากวันก่อนหน้า** ให้เป็นรายไอเทมโดยอัตโนมัติ")
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
