import pandas as pd
import streamlit as st

def load_and_process_inventory(file_path, item_column_name):
    """
    ฟังก์ชันสำหรับอ่านและทำความสะอาดข้อมูลจากไฟล์ CSV
    """
    try:
        # อ่านไฟล์ CSV โดยข้าม 2 บรรทัดแรกที่เป็นคำแนะนำ (Instruction)
        # ใช้ utf-8-sig เพื่อรองรับภาษาไทยได้อย่างสมบูรณ์
        df = pd.read_csv(file_path, skiprows=2, encoding='utf-8-sig')
        
        # เปลี่ยนชื่อคอลัมน์แรกสุดให้เป็นชื่อรายการ (เนื่องจากหลัง skiprow คอลัมน์แรกจะชื่อ Unnamed: 0)
        df.rename(columns={df.columns[0]: item_column_name}, inplace=True)
        
        # ลบแถวที่ไม่มีชื่อรายการออก
        df = df.dropna(subset=[item_column_name])
        
        # ดึงรายชื่อคอลัมน์ที่เป็น "วันที่" (ตั้งแต่คอลัมน์ที่ 2 เป็นต้นไป)
        date_columns = df.columns[1:]
        
        # ค้นหาวันที่ล่าสุดที่มีการกรอกข้อมูล (เริ่มหาจากหลังสุดมาหน้าสุด)
        latest_date = date_columns[0]
        valid_date_cols = []
        
        for col in reversed(date_columns):
            if df[col].notna().any():
                latest_date = col
                break
                
        # เก็บรายการวันที่ทั้งหมดตั้งแต่เริ่มจนถึงวันที่ล่าสุด
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
    """
    ฟังก์ชันสำหรับแสดงตารางข้อมูลในรูปแบบที่ทันสมัย เข้าใจง่าย
    """
    if df is None or df.empty:
        return

    # สร้าง DataFrame ใหม่สำหรับแสดงผลเท่านั้น เพื่อความสะอาดตา
    display_df = pd.DataFrame()
    display_df['รายการ'] = df[item_col]
    
    # ข้อมูลคงเหลือล่าสุด (แทนที่ค่าว่างด้วย 0)
    display_df['คงเหลือล่าสุด'] = df[latest_date].fillna(0).astype(int)
    
    # สร้างข้อมูลประวัติย้อนหลังสำหรับแสดงเป็นกราฟเส้น (Sparkline)
    history_data = []
    for index, row in df.iterrows():
        # ดึงค่าตั้งแต่วันแรกจนถึงวันที่ล่าสุด แปลงเป็น float ตัวไหนว่างให้เป็น 0
        hist = [float(x) if pd.notna(x) else 0.0 for x in row[valid_date_cols].values]
        history_data.append(hist)
        
    display_df['ประวัติย้อนหลัง'] = history_data

    # วาดตารางโดยใช้ UI ใหม่ล่าสุดของ Streamlit
    st.dataframe(
        display_df,
        column_config={
            "รายการ": st.column_config.TextColumn(
                "📝 ชื่อรายการ", 
                width="large"
            ),
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
    """
    ฟังก์ชันหลักสำหรับเรียกใช้งานเพื่อแสดงผลบนหน้าจอ
    (นำฟังก์ชันนี้ไปเรียกใช้ใน Tab ของ app.py)
    """
    st.markdown("## 🏥 ระบบรายงานเวชภัณฑ์และยาคงคลัง (PM 2.5)")
    st.markdown("แสดงข้อมูลจำนวนคงคลัง **เฉพาะข้อมูลล่าสุด** พร้อมกราฟแนวโน้มย้อนหลังเพื่อให้ดูง่ายและสบายตา")
    st.divider()

    # ชื่อไฟล์ CSV
    med_supplies_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
    medicines_file = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

    # โหลดข้อมูล
    df_sup, latest_date_sup, valid_cols_sup = load_and_process_inventory(med_supplies_file, "รายการพัสดุการแพทย์")
    df_med, latest_date_med, valid_cols_med = load_and_process_inventory(medicines_file, "รายการยา")

    # แสดงวันที่อัปเดตล่าสุดที่ด้านบน
    latest_update = latest_date_sup if latest_date_sup else "ไม่มีข้อมูล"
    st.info(f"🔄 **อัปเดตข้อมูลล่าสุดเมื่อ:** {latest_update}")

    # สร้าง Sub-tabs แบ่งหมวดหมู่ให้สวยงาม
    tab_sup, tab_med = st.tabs(["📦 พัสดุการแพทย์", "💊 รายการยา"])

    with tab_sup:
        st.subheader("พัสดุการแพทย์คงคลัง")
        display_modern_inventory_table(df_sup, "รายการพัสดุการแพทย์", latest_date_sup, valid_cols_sup)

    with tab_med:
        st.subheader("รายการยาคงคลัง")
        display_modern_inventory_table(df_med, "รายการยา", latest_date_med, valid_cols_med)
