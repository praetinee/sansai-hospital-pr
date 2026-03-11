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
    """ฟังก์ชันแสดงตารางเวชภัณฑ์แบบ Custom HTML เพื่อรองรับการจัดกึ่งกลาง 100%"""
    if df is None or df.empty or not date_columns:
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบลิงก์ Google Sheet")
        return

    # 1. หาวันที่ที่มีการกรอกข้อมูลระดับภาพรวม (Global Filled Dates)
    filled_dates = []
    for col in date_columns:
        if any(parse_value(val) is not None for val in df[col]):
            filled_dates.append(col)
            
    if not filled_dates:
        st.info("ไม่มีข้อมูลการอัปเดตในตาราง")
        return

    # 2. กำหนดวันล่าสุด และ วันก่อนหน้าล่าสุด
    global_latest_date = filled_dates[-1]
    global_prev_date = filled_dates[-2] if len(filled_dates) > 1 else None

    # สร้างชื่อคอลัมน์
    stock_col_name = f"คงคลัง ณ วันที่ {global_latest_date}"
    change_col_name = "การเพิ่มขึ้น/ลดลง (จากข้อมูลล่าสุด)"

    html_rows = ""
    
    # 3. วนลูปเช็คข้อมูลทีละไอเทม
    for index, row in df.iterrows():
        item_name = str(row[item_col]).replace('<', '&lt;').replace('>', '&gt;')
        
        # ฟังก์ชันย่อยสำหรับดึง "ยอดคงเหลือล่าสุด" จนถึงวันที่กำหนด
        def get_value_up_to(target_date):
            last_val = 0
            for col in date_columns:
                val = parse_value(row[col])
                if val is not None:
                    last_val = val
                if col == target_date:
                    break
            return last_val

        # ดึงยอดล่าสุด ณ วันที่กำหนด
        current_val = get_value_up_to(global_latest_date)
        delta_str = "-"

        # ดึงยอดของวันก่อนหน้า และหาผลต่าง
        if global_prev_date:
            prev_val = get_value_up_to(global_prev_date)
            diff = current_val - prev_val
            
            # จัด Format และใส่สีสันให้เข้าใจง่าย (เขียวเพิ่ม แดงลด)
            if diff > 0:
                delta_str = f"🔺 <span style='color: #059669; font-weight: bold;'>+{int(diff):,}</span>"
            elif diff < 0:
                delta_str = f"🔻 <span style='color: #dc2626; font-weight: bold;'>{int(diff):,}</span>"
            else:
                delta_str = f"➖ <span style='color: #64748b;'>0</span>"
        else:
            delta_str = f"➖ <span style='color: #64748b;'>0</span>"

        # ประกอบข้อมูลทีละบรรทัด (บังคับกึ่งกลางที่เซลล์ด้วย class="text-center")
        html_rows += f"""
            <tr>
                <td>{item_name}</td>
                <td class="text-center" style="font-weight: 500;">{int(current_val):,}</td>
                <td class="text-center">{delta_str}</td>
            </tr>
        """

    # 4. สร้างตาราง HTML สไตล์ Modern
    help_text = f"เปรียบเทียบส่วนต่างระหว่าง {global_latest_date} กับ {global_prev_date}" if global_prev_date else "เพิ่งมีการบันทึกข้อมูลวันแรก"
    
    html_table = f"""
    <style>
        .inventory-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 20px 0;
            font-family: inherit;
        }}
        .inventory-table th {{
            background-color: #f1f5f9;
            color: #334155;
            font-size: 1.05rem;
            padding: 12px 15px;
            border-bottom: 2px solid #cbd5e1;
        }}
        .inventory-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
            color: #1e293b;
        }}
        .inventory-table tr:hover td {{
            background-color: #f8fafc;
        }}
        .text-center {{
            text-align: center !important;
        }}
    </style>
    <div style="overflow-x: auto; background-color: white; border-radius: 8px; border: 1px solid #e2e8f0;">
        <table class="inventory-table">
            <thead>
                <tr>
                    <th style="text-align: left;">📝 ชื่อรายการ</th>
                    <th class="text-center" title="ข้อมูลล่าสุด">📦 {stock_col_name}</th>
                    <th class="text-center" title="{help_text}">📊 {change_col_name}</th>
                </tr>
            </thead>
            <tbody>
                {html_rows}
            </tbody>
        </table>
    </div>
    """

    # แสดงผลตารางด้วยคำสั่ง Markdown แบบอนุญาตให้ใช้ HTML
    st.markdown(html_table, unsafe_allow_html=True)

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
