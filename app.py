import streamlit as st
import pandas as pd
from dashboard import render_dashboard
from flow import render_flow
from roles import render_roles

# ------------------------------------------------------------------
# ฟังก์ชันระบบจัดการเวชภัณฑ์คงคลัง
# ------------------------------------------------------------------
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
    """ฟังก์ชันอ่านและดึงข้อมูลเฉพาะวันที่ล่าสุดแบบยืดหยุ่น"""
    try:
        # แก้ปัญหาจำนวนลูกน้ำไม่เท่ากันในแต่ละบรรทัด โดยบังคับสร้างคอลัมน์เผื่อไว้ 100 คอลัมน์
        df_raw = pd.read_csv(file_path, names=range(100), encoding='utf-8-sig', dtype=str)
        
        # ค้นหาแถวที่เป็น Header ของวันที่จริงๆ (มองหาชื่อย่อเดือนภาษาไทย)
        thai_months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
        header_idx = -1
        
        for i, row in df_raw.iterrows():
            # รวมข้อความในแถวเพื่อตรวจสอบหาชื่อเดือน
            row_str = " ".join([str(x) for x in row.values if pd.notna(x)])
            if any(month in row_str for month in thai_months):
                header_idx = i
                break

        if header_idx == -1:
            return None, None, None

        # ดึงบรรทัดที่เจอมาวิเคราะห์คอลัมน์
        raw_columns = list(df_raw.iloc[header_idx].values)
        
        # เก็บลำดับ (index) ของคอลัมน์ที่มีวันที่จริงๆ ป้องกันปัญหาคอลัมน์ว่างหรือชื่อซ้ำ
        valid_col_indices = [0] # index 0 บังคับเป็นชื่อรายการ
        date_columns = []
        
        for idx, col in enumerate(raw_columns):
            if idx == 0: continue
            col_str = str(col).strip()
            if pd.notna(col) and col_str not in ['nan', 'None', '']:
                if col not in date_columns: # ป้องกันคอลัมน์วันที่ซ้ำ
                    date_columns.append(col)
                    valid_col_indices.append(idx)

        if not date_columns:
            return None, None, None

        # ตัดข้อมูลเฉพาะคอลัมน์ที่ใช้งาน (อ้างอิงตำแหน่ง index เดิม) และตัดส่วนหัวทิ้ง
        df = df_raw.iloc[header_idx + 1:, valid_col_indices].copy()
        df.columns = [item_column_name] + date_columns
            
        # ลบแถวที่ชื่อรายการเป็นค่าว่าง หรือคำว่า nan
        df = df.dropna(subset=[item_column_name])
        df = df[df[item_column_name].astype(str).str.strip().str.lower() != 'nan']
        df = df[df[item_column_name].astype(str).str.strip() != '']
        
        # หาวันที่ล่าสุดที่มีข้อมูลตัวเลขกรอกไว้จริงๆ (เช็คจากหลังมาหน้า)
        latest_date = None
        valid_date_cols = []
        
        for col in reversed(date_columns):
            has_data = False
            for val in df[col]:
                val_str = str(val).strip().replace(',', '')
                if pd.notna(val) and val_str not in ['', 'nan', 'None', '-']:
                    try:
                        float(val_str) # ถ้าแปลงเป็นตัวเลขได้ แปลว่ามีการกรอกข้อมูลแล้ว
                        has_data = True
                        break
                    except ValueError:
                        pass
            if has_data:
                latest_date = col
                break
                
        # ถ้ารู้วันที่ล่าสุดแล้ว ให้เก็บเฉพาะวันที่ตั้งแต่เริ่มต้นจนถึงวันล่าสุดเพื่อทำกราฟ
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
        st.warning("ไม่พบข้อมูลที่จะแสดงผล กรุณาตรวจสอบรูปแบบไฟล์ CSV")
        return

    display_df = pd.DataFrame()
    display_df['รายการ'] = df[item_col]
    
    # ดึงข้อมูลคงเหลือล่าสุดแปลงเป็นตัวเลขอย่างปลอดภัย
    display_df['คงเหลือล่าสุด'] = df[latest_date].apply(to_float).astype(int)
    
    # สร้างประวัติย้อนหลังเป็น List สำหรับแสดงเป็นกราฟ
    history_data = []
    for index, row in df.iterrows():
        hist = [to_float(x) for x in row[valid_date_cols].values]
        history_data.append(hist)
        
    display_df['ประวัติย้อนหลัง'] = history_data

    # แสดงผลตารางด้วย UI แบบใหม่ของ Streamlit
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

# ------------------------------------------------------------------
# โค้ดเดิมทั้งหมดของคุณ (ไม่มีการแก้ไข)
# ------------------------------------------------------------------

# 1. ตั้งค่าหน้าเว็บ Streamlit ให้เป็นแบบกว้างสุด (Wide)
st.set_page_config(
    page_title="PM2.5 Action Plan - โรงพยาบาลสันทราย",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ปรับแต่ง CSS แบบขั้นสุด
hide_streamlit_style = """
<style>
    /* อนุญาตให้แสดง Header ของ Streamlit เพื่อใช้เมนู Tool ได้ */
    /* header {visibility: hidden !important;} */
    footer {visibility: hidden !important;}

    /* ปรับระยะขอบของ Streamlit Container เพิ่ม padding-top เพื่อไม่ให้ถูก Header บัง */
    .block-container {
        padding-top: 4rem !important; 
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* ตกแต่ง Tabs ของ Streamlit ให้ดูทันสมัยและไม่โดนตัด */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        padding: 0 1rem;
        background-color: transparent;
        flex-wrap: wrap; /* รองรับหน้าจอมือถือให้ Tab ปัดบรรทัดได้ */
    }
    .stTabs [data-baseweb="tab"] {
        /* เปลี่ยนจากการล็อกความสูง (height) เป็นใช้ padding แทน เพื่อป้องกันหน้าจอตัดขอบ */
        padding: 0.75rem 1.5rem;
        border-radius: 10px 10px 0 0;
        background-color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: bold;
        color: #475569;
        border: 1px solid #cbd5e1;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #059669 !important;
        color: white !important;
        border-color: #059669 !important;
    }
    
    /* ลบขอบ iframe */
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 3. จัดการแสดงผล Tabs และเรียกใช้โมดูล (อัปเดต: เพิ่มแท็บเวชภัณฑ์คงคลัง)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 แผนการดำเนินงาน", 
    "🔄 ขั้นตอนการให้บริการ", 
    "🗺️ บทบาทของแต่ละหน่วยงาน",
    "📦 เวชภัณฑ์คงคลัง"
])

with tab1:
    # เรียกใช้ฟังก์ชันจากไฟล์ dashboard.py
    render_dashboard()
    
with tab2:
    # เรียกใช้ฟังก์ชันจากไฟล์ flow.py
    render_flow()

with tab3:
    # เรียกใช้ฟังก์ชันจากไฟล์ roles.py 
    render_roles()

with tab4:
    # ส่วนแสดงผลเวชภัณฑ์คงคลังที่เพิ่มใหม่
    st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
    st.markdown("แสดงข้อมูลจำนวนคงคลัง **เฉพาะข้อมูลล่าสุด** พร้อมกราฟแนวโน้มย้อนหลังเพื่อให้ดูง่ายและสบายตา")
    st.divider()

    # ชื่อไฟล์อ้างอิงตรงตามที่คุณอัปโหลดใช้งาน
    med_supplies_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
    medicines_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

    # ดึงข้อมูลมาประมวลผล
    df_sup, latest_date_sup, valid_cols_sup = load_and_process_inventory(med_supplies_file, "รายการพัสดุการแพทย์")
    df_med, latest_date_med, valid_cols_med = load_and_process_inventory(medicines_file, "รายการยา")

    # แจ้งเตือนวันที่อัปเดตข้อมูลล่าสุด
    latest_update = latest_date_sup if latest_date_sup else "ไม่มีข้อมูล"
    st.info(f"🔄 **อัปเดตข้อมูลล่าสุดเมื่อ:** {latest_update}")

    # แบ่งหมวดหมู่พัสดุและยา
    tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

    with tab_sup:
        display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", latest_date_sup, valid_cols_sup)

    with tab_med:
        display_modern_inventory_table(df_med, "รายการยา", latest_date_med, valid_cols_med)
