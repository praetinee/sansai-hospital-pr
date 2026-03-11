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
    """ฟังก์ชันอ่านข้อมูล อ้างอิงจากโครงสร้าง: แถว 1=คำอธิบาย, แถว 2-3=หัวตาราง"""
    try:
        # ใช้ header=[1, 2] เพื่อกำหนดให้ดึงหัวตารางจากแถวที่ 2 และ 3 (index 1 และ 2)
        # Pandas จะทำการข้ามแถวแรกที่เป็น Instruction ไปโดยอัตโนมัติ
        df_raw = pd.read_csv(file_path, header=[1, 2], encoding='utf-8-sig', dtype=str)
        
        # คอลัมน์ที่ 1 เป็นต้นไป (Level 1) คือข้อมูลของวันที่
        raw_dates = df_raw.columns.get_level_values(1)[1:]
        
        valid_col_indices = [0] # index 0 บังคับเป็นชื่อรายการ
        date_columns = []
        
        for i, col in enumerate(raw_dates):
            col_str = str(col).strip()
            # กรองเฉพาะชื่อคอลัมน์ที่ใช้งานได้
            if pd.notna(col) and not col_str.startswith('Unnamed'):
                date_columns.append(col_str)
                valid_col_indices.append(i + 1)

        if not date_columns:
            return None, None, None

        # ตัดข้อมูลมาเฉพาะคอลัมน์ชื่อรายการ + วันที่
        df = df_raw.iloc[:, valid_col_indices].copy()
        df.columns = [item_column_name] + date_columns
            
        # ลบแถวที่ชื่อรายการเป็นค่าว่าง
        df = df.dropna(subset=[item_column_name])
        df = df[df[item_column_name].astype(str).str.strip().str.lower() != 'nan']
        df = df[df[item_column_name].astype(str).str.strip() != '']
        
        latest_date = None
        valid_date_cols = []
        
        # หาวันที่ล่าสุดที่มีข้อมูลตัวเลขกรอกไว้จริงๆ (เช็คจากหลังมาหน้า)
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
                
        # หากพบวันที่ล่าสุด จะเก็บข้อมูลตั้งแต่วันแรกถึงวันล่าสุดเพื่อใช้สร้างกราฟเส้น
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
