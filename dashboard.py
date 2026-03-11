import streamlit as st
import pandas as pd

# ==========================================
# 🚀 ฟังก์ชันสำหรับดึงและทำความสะอาดข้อมูล (Data Processing)
# ==========================================
@st.cache_data
def load_inventory_data(filepath):
    try:
        # ข้าม 2 บรรทัดแรก (คำอธิบายและหัวตารางเดิม) 
        # เพื่อใช้แถวที่มีวันที่ (เช่น 8 มี.ค., 9 มี.ค.) เป็นคอลัมน์ Header
        df = pd.read_csv(filepath, skiprows=2)

        # ตั้งชื่อคอลัมน์แรกที่ไม่มีชื่อ (Unnamed: 0) เป็น 'รายการ'
        df.rename(columns={df.columns[0]: 'รายการ'}, inplace=True)

        # ลบแถวที่ไม่มีข้อมูลชื่อรายการออก
        df = df.dropna(subset=['รายการ'])

        # หาคอลัมน์วันที่ล่าสุด (เช็คจากขวาสุดมาซ้าย หาคอลัมน์ที่มีข้อมูลอยู่)
        date_cols = df.columns[1:]
        latest_date = date_cols[-1]
        for col in reversed(date_cols):
            if not df[col].isnull().all():
                latest_date = col
                break

        # สร้างตารางข้อมูลเฉพาะวันล่าสุด
        df_latest = df[['รายการ', latest_date]].copy()
        df_latest.columns = ['รายการ', 'จำนวนคงเหลือ']
        
        # แปลงค่าตัวเลขให้สวยงาม (จัดการค่าว่างให้กลายเป็น 0)
        df_latest['จำนวนคงเหลือ'] = pd.to_numeric(df_latest['จำนวนคงเหลือ'], errors='coerce').fillna(0).astype(int)

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

    # ระบุชื่อไฟล์ CSV (อ้างอิงจากไฟล์ที่คุณอัปโหลด)
    file_supply = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - พัสดุการแพทย์.csv"
    file_medicine = "ลงข้อมูลคลังเวชภัณฑ์รพ.สันทรายPM2.5 - ยา.csv"

    # โหลดข้อมูล
    df_sup_hist, df_sup_latest, date_sup = load_inventory_data(file_supply)
    df_med_hist, df_med_latest, date_med = load_inventory_data(file_medicine)

    # แบ่งหน้าจอเป็น 2 คอลัมน์ซ้ายขวา
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏥 พัสดุการแพทย์")
        if df_sup_latest is not None:
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
            st.error("ไม่สามารถโหลดข้อมูลพัสดุการแพทย์ได้ (โปรดตรวจสอบชื่อไฟล์)")

    with col2:
        st.subheader("💊 รายการยา")
        if df_med_latest is not None:
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
            st.error("ไม่สามารถโหลดข้อมูลยาได้ (โปรดตรวจสอบชื่อไฟล์)")

# ==========================================
# ⚙️ ตัวอย่างการนำไปใช้รวมกับ Dashboard เดิมของคุณ
# ==========================================
def main():
    # สมมติว่าโครงสร้างเดิมของคุณมี Tabs อยู่แบบนี้
    # ให้คุณเพิ่ม "📦 เวชภัณฑ์คงคลัง" เข้าไปในลิสต์ st.tabs ของคุณ
    tab1, tab_inventory = st.tabs([
        "📊 Dashboard หลัก (โค้ดเดิมของคุณ)", 
        "📦 เวชภัณฑ์คงคลัง" # <- Tab ที่เพิ่มใหม่
    ])

    with tab1:
        st.write("พื้นที่สำหรับวางโค้ดหน้า Dashboard อันเดิมของคุณ")
        # [ ก๊อบปี้โค้ดการแสดงผลเดิมของคุณมาไว้ตรงนี้ได้เลยโดยไม่ต้องแก้ไขใดๆ ]

    with tab_inventory:
        # เรียกใช้ฟังก์ชันที่สร้างไว้ด้านบน
        render_inventory_tab()

if __name__ == "__main__":
    main()
