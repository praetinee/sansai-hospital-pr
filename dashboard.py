import streamlit as st
import pandas as pd

# ==========================================
# 🚀 ฟังก์ชันสำหรับดึงและทำความสะอาดข้อมูล (Data Processing)
# ==========================================
@st.cache_data
def load_inventory_data(filepath):
    try:
        # อ่านข้อมูลทั้งหมดแบบ String เพื่อป้องกันปัญหา Header ซ้อนกันหรือคอลัมน์เลื่อน
        raw_df = pd.read_csv(filepath, header=None, dtype=str)
        
        # 1. ค้นหาแถวที่เป็น Header (แถวที่มีชื่อเดือน เช่น มี.ค., เม.ย.)
        header_idx = 0
        for i, row in raw_df.iterrows():
            row_str = " ".join(row.fillna("").astype(str).values)
            # ค้นหาคีย์เวิร์ดเดือน เพื่อระบุว่านี่คือแถววันที่
            if any(m in row_str for m in ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']):
                header_idx = i
                break
        
        # 2. จัดการดึงชื่อคอลัมน์ออกมาให้ถูกต้อง
        headers = []
        for j, val in enumerate(raw_df.iloc[header_idx].values):
            val_str = str(val).strip() if pd.notna(val) else ""
            if val_str == "" or val_str.lower() == "nan":
                # หากเป็นคอลัมน์แรกให้ตั้งชื่อว่า 'รายการ'
                if j == 0:
                    headers.append("รายการ")
                else:
                    headers.append(f"Unnamed_{j}")
            else:
                headers.append(val_str)
        
        # 3. ตัดเฉพาะแถวข้อมูลจริงๆ (ลบ Header และคำอธิบายทิ้ง)
        df = raw_df.iloc[header_idx + 1:].copy()
        df.columns = headers
        
        # ทำให้แน่ใจว่าคอลัมน์แรกชื่อ 'รายการ' เสมอ
        if 'รายการ' not in df.columns:
            df.rename(columns={df.columns[0]: 'รายการ'}, inplace=True)
            
        # ลบแถวที่ไม่มีชื่อรายการ (แถวว่าง) ออก
        df = df.dropna(subset=['รายการ'])
        df = df[df['รายการ'].astype(str).str.strip() != ""]
        df = df[df['รายการ'].astype(str).str.lower() != "nan"]
        
        # 4. หาคอลัมน์วันที่ล่าสุดที่มีข้อมูล
        # ตัดคอลัมน์ 'รายการ' และ 'Unnamed' ออก จะเหลือแค่วันที่
        date_cols = [col for col in df.columns if col != 'รายการ' and not col.startswith('Unnamed_')]
        latest_date = date_cols[-1] if date_cols else "ไม่มีข้อมูลวันที่"
        
        # ไล่เช็คจากวันที่ล่าสุดย้อนกลับมา เพื่อหาวันที่มีตัวเลขถูกกรอกแล้วจริงๆ
        for col in reversed(date_cols):
            # ตรวจสอบว่าคอลัมน์นี้มีตัวเลขกรอกไว้หรือไม่ (ข้ามช่องว่าง)
            valid_data = df[col].replace(["", "nan", "NaN", "-"], pd.NA).dropna()
            if not valid_data.empty:
                latest_date = col
                break
                
        # 5. สร้างตารางสรุปยอดล่าสุด
        if date_cols:
            df_latest = df[['รายการ', latest_date]].copy()
            df_latest.columns = ['รายการ', 'จำนวนคงเหลือ']
            # ลบลูกน้ำ (,) ออกแล้วแปลงค่าให้เป็นตัวเลข (ช่องว่างจะกลายเป็น 0)
            df_latest['จำนวนคงเหลือ'] = pd.to_numeric(df_latest['จำนวนคงเหลือ'].astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)
        else:
            df_latest = pd.DataFrame(columns=['รายการ', 'จำนวนคงเหลือ'])
            
        return df, df_latest, latest_date
    except Exception as e:
        return None, None, str(e)

# ==========================================
# 🎨 ฟังก์ชันสำหรับแสดงผลหน้า UI เวชภัณฑ์คงคลัง
# ==========================================
def render_inventory_tab():
    st.markdown("## 📦 ระบบจัดการเวชภัณฑ์และยาคงคลัง")
    st.markdown("แสดงผลข้อมูลเฉพาะ **ยอดคงเหลือของวันที่อัปเดตล่าสุด** เพื่อให้ติดตามสถานการณ์ได้รวดเร็วและแม่นยำ")
    st.divider()

    # ระบุชื่อไฟล์ CSV
    file_supply = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
    file_medicine = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

    # โหลดข้อมูล
    df_sup_hist, df_sup_latest, date_sup = load_inventory_data(file_supply)
    df_med_hist, df_med_latest, date_med = load_inventory_data(file_medicine)

    # แบ่งหน้าจอเป็น 2 คอลัมน์ซ้ายขวา
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏥 พัสดุการแพทย์")
        if df_sup_latest is not None and not df_sup_latest.empty:
            st.info(f"📅 อัปเดตล่าสุด: **{date_sup}**")
            
            # ตารางแสดงข้อมูลล่าสุด
            st.dataframe(
                df_sup_latest,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "รายการ": st.column_config.TextColumn("รายการพัสดุ", width="large"),
                    "จำนวนคงเหลือ": st.column_config.NumberColumn("คงเหลือ (หน่วย)", format="%d")
                }
            )
            
            # ส่วนซ่อน/แสดงข้อมูลย้อนหลัง
            with st.expander("🕒 ดูประวัติพัสดุการแพทย์ย้อนหลังทั้งหมด"):
                st.dataframe(df_sup_hist, use_container_width=True, hide_index=True)
        else:
            st.error("ไม่พบข้อมูลพัสดุการแพทย์ (ตารางอาจว่างเปล่า)")

    with col2:
        st.subheader("💊 รายการยา")
        if df_med_latest is not None and not df_med_latest.empty:
            st.success(f"📅 อัปเดตล่าสุด: **{date_med}**")
            
            # ตารางแสดงข้อมูลล่าสุด
            st.dataframe(
                df_med_latest,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "รายการ": st.column_config.TextColumn("รายการยา", width="large"),
                    "จำนวนคงเหลือ": st.column_config.NumberColumn("คงเหลือ (หน่วย)", format="%d")
                }
            )
            
            # ส่วนซ่อน/แสดงข้อมูลย้อนหลัง
            with st.expander("🕒 ดูประวัติรายการยาย้อนหลังทั้งหมด"):
                st.dataframe(df_med_hist, use_container_width=True, hide_index=True)
        else:
            st.error("ไม่พบข้อมูลยา (ตารางอาจว่างเปล่า)")

# ==========================================
# ⚙️ ฟังก์ชันหลักที่ app.py จะดึงไปใช้งาน
# ==========================================
def render_dashboard():
    # โค้ดส่วนนี้จะสร้าง Tab สองอัน 
    tab1, tab_inventory = st.tabs([
        "📊 Dashboard หลัก (ข้อมูลเดิม)", 
        "📦 เวชภัณฑ์คงคลัง"
    ])

    with tab1:
        # 💡 นำโค้ดเดิมที่เคยอยู่ในไฟล์ dashboard.py มาวางใต้บรรทัดนี้ได้เลยครับ
        st.write("พื้นที่สำหรับหน้า Dashboard เดิม")

    with tab_inventory:
        # เรียกใช้ส่วนแสดงผลคลังเวชภัณฑ์
        render_inventory_tab()
